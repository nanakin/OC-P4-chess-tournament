from chess_tournament.models.model import Model
from .states import State
from .actions.players import PlayerController
from .actions.matches import MatchesController
from .actions.tournaments import TournamentsController
from .actions.participants import ParticipantsController
from .actions.main import MainMenuController
from .fill_db import FillDB  # temporary


class Controller(PlayerController, MatchesController, TournamentsController, ParticipantsController, MainMenuController, FillDB):

    def __init__(self, view, data_path):
        # view
        self.view = view
        # model
        self.model = Model(data_path)
        self.add_default_entries()  # temporary
        # controller
        self.status = State.MAIN_MENU
        self.context = None

    def run(self):

        state_to_action = {
            State.MAIN_MENU: self.show_main_menu,
            State.MANAGE_PLAYER_MENU: self.show_manage_player_menu,
            State.EDIT_PLAYER_MENU: self.show_edit_player_menu,
            State.ADD_PLAYER_MENU: self.show_add_player_menu,
            State.LIST_PLAYERS_MENU: self.show_list_players_menu,
            State.MANAGE_TOURNAMENTS_MENU: self.show_manage_tournaments_menu,
            State.LIST_TOURNAMENTS_MENU: self.show_list_tournaments_menu,
            State.MANAGE_TOURNAMENT_MENU: self.show_manage_tournament_menu,
            State.MANAGE_UNREADY_TOURNAMENT_MENU: self.show_manage_unready_tournament_menu,
            State.ADD_TOURNAMENT_MENU: self.show_tournament_registration,
            State.SELECT_TOURNAMENT_MENU: self.show_select_tournament_menu,
            State.MANAGE_PARTICIPANTS_MENU: self.show_manage_participants_menu,
            State.ADD_PARTICIPANT_MENU: self.show_add_participant_menu,
            State.DELETE_PARTICIPANT_MENU: self.show_delete_participant_menu,
            State.REGISTER_MATCH_SCORE_MENU: self.show_register_match_score_menu
        }

        while self.status != State.QUIT:
            state_to_action[self.status]()
