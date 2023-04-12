"""Define chess players related user interface."""

import questionary as q
from ..requests import Request, RequestAnswer
from ..validators import (
    non_empty_alphabet_validator,
    past_date_validator,
    national_identifier_validator,
)
from .common import clear_screen_and_show_log, print_title


class PlayerMenus:
    """Players related View’s mixin class."""

    @clear_screen_and_show_log
    def show_manage_player_menu(self) -> RequestAnswer:
        """Display a select menu : add/edit/list players or back."""
        print_title("Players menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Add player", value=Request.ADD_PLAYER),
                q.Choice(title="Edit player", value=Request.EDIT_PLAYER),
                q.Choice(title="List players", value=Request.LIST_PLAYERS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MAIN_MENU),
            ],
        )
        return question.ask()

    @clear_screen_and_show_log
    def show_player_selection(self, players_id):
        """Display an autocomplete question for players ID."""
        print_title("Player selection menu")
        question = q.autocomplete(
            "Enter the player ID :",
            choices=players_id,
            validate=lambda x: x in players_id,
        )
        return Request.SELECTED_PLAYER, question.ask()

    @clear_screen_and_show_log
    def show_player_registration(self) -> RequestAnswer:
        """Prompt 4 input questions (first/last name, birthdate, ID) with user entries validation."""
        print_title("Player registration menu")
        add_player_questions = [
            {
                "type": "text",
                "name": "first_name",
                "qmark": ">",
                "message": "Enter player's first name :",
                "validate": non_empty_alphabet_validator,
            },
            {
                "type": "text",
                "name": "last_name",
                "qmark": ">",
                "message": "Enter player's last name :",
                "validate": non_empty_alphabet_validator,
            },
            {
                "type": "text",
                "name": "birth_date",
                "qmark": ">",
                "message": "Enter player's date of birth (YYYY-MM-DD):",
                "validate": past_date_validator,
            },
            {
                "type": "text",
                "name": "identifier",
                "qmark": ">",
                "message": "Enter player's national identifier :",
                "validate": national_identifier_validator,
            },
        ]
        raw_player_data = q.prompt(add_player_questions)
        if not raw_player_data:  # ctrl-c
            return Request.MANAGE_PLAYER, None
        else:
            return Request.REGISTER_PLAYER_DATA, raw_player_data

    @clear_screen_and_show_log
    def show_edit_player_menu(self, player_info):
        """Display a menu to select the attribute to change then an input question (with user entry validation)."""
        print_title("Player edition menu")
        what_to_edit = q.select(
            "What to edit ?",
            choices=[
                q.Choice(title="First name", value="first_name"),
                q.Choice(title="Last name", value="last_name"),
                q.Choice(title="Birth date", value="birth_date"),
                q.Choice(title="Cancel"),
            ],
        )
        answer = what_to_edit.ask()
        if answer == "first_name":
            player_info["first_name"] = q.text(
                "Enter player's new first name: ", validate=non_empty_alphabet_validator
            ).ask()
        elif answer == "last_name":
            player_info["last_name"] = q.text(
                "Enter player's new last name: ", validate=non_empty_alphabet_validator
            ).ask()
        elif answer == "birth_date":
            player_info["birth_date"] = q.text("Enter player's new birth date: ", validate=past_date_validator).ask()
        else:
            return Request.MANAGE_PLAYER, None
        return Request.REGISTER_PLAYER_DATA, player_info
