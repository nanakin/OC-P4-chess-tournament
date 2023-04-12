"""Define backup manager class(es) and function(s)."""

import json
import logging
from .chessdata.player import Player
from .chessdata.tournament import Tournament


def save_at_the_end(players_file=False, tournaments_file=False):
    """Decorator that saves data to JSON file(s) once the function ended."""

    def save_at_the_end_decorator(function):
        def wrapper(self, *args, **kwargs):
            return_values = function(self, *args, **kwargs)
            self.save(players_file, tournaments_file)
            return return_values

        return wrapper

    return save_at_the_end_decorator


def save_to_json(data, path):
    """Write compatible JSON data to JSON file."""
    try:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=2)
    except FileNotFoundError:
        return False, None
    else:
        return True, path.absolute()


class BackupManager:
    """Save and load system."""

    # to-do : store data_path attribute in this class.
    # def __init__(self, path=""):
    #    self.path = path

    def save(self, players_file=False, tournaments_file=False):
        """Encode model’s data then write them to JSON file(s).

        This function is called by the save_at_the_end decorator used on modifying data Model’s methods."""
        if players_file:
            players_encoded = []
            for player in self.players.values():
                players_encoded.append(player.encode())
            is_ok, abs_path = save_to_json(path=(self.data_path / "players.json"), data=players_encoded)
            logging.debug(f"{is_ok=}: players autosave in {self.data_path}")
        if tournaments_file:
            tournaments_encoded = []
            for tournament in self.tournaments:
                tournaments_encoded.append(tournament.encode())
            # logging.debug(tournaments_encoded)
            is_ok, abs_path = save_to_json(path=(self.data_path / "tournaments.json"), data=tournaments_encoded)
            logging.debug(f"{is_ok=}: tournaments autosave in {self.data_path}")

    def load(self):
        """Load model’s data from JSON files."""
        # TODO: review the function structure

        def json_load_data(filename):
            """Load data from a given JSON file."""
            with open(filename, "r") as json_file:
                encoded_data = json.load(json_file)
            return encoded_data

        players_file = self.data_path / "players.json"
        tournaments_file = self.data_path / "tournaments.json"
        try:
            encoded_players = json_load_data(players_file)
        except FileNotFoundError as err:
            return False, err
        else:
            for encoded_player in encoded_players:
                player = Player.decode(encoded_player)
                self.players[player.identifier] = player

        try:
            encoded_tournaments = json_load_data(tournaments_file)
        except FileNotFoundError as err:
            return False, err
        else:
            for encoded_tournament in encoded_tournaments:
                tournament = Tournament.decode(encoded_tournament)
                self.tournaments.append(tournament)
            logging.debug(f"{len(encoded_tournaments)} tournaments loaded")
        return len(encoded_players), len(encoded_tournaments)
