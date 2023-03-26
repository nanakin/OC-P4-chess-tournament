from enum import Enum
from typing import TypeAlias

Request = Enum("Request", [
    "EXIT_APP",
    "EXIT_LOCAL_MENU",
    "MAIN_MENU",
    "SAVE",
    "MANAGE_PLAYER",
    "ADD_PLAYER",
    "REGISTER_PLAYER_DATA",
    "LIST_PLAYERS",
    "EDIT_PLAYER",
    "PRINT_PLAYERS",
    "EXPORT_PLAYERS",
    "SHOW_SELECT_PLAYER",
    "SELECTED_PLAYER",
    "CONFIRM",
    "SHOW_CONFIRM_PLAYER",
    "SHOW_EDIT_PLAYER_MENU",
    "MANAGE_TOURNAMENT",
    "ADD_TOURNAMENT",
    "EDIT_TOURNAMENT",
    "LIST_TOURNAMENTS",
    "LIST_MATCHES",
    "LAUNCH_PARTICIPANT_MENU",
    "ADD_PARTICIPANT",
    "GET_MATCHES_LIST",
    "REGISTER_MATCH_SCORE",
    "CHOSEN_TOURNAMENT",
    "SELECTED_TOURNAMENT",
    "LIST_ROUNDS_SCORES",
    "MANAGE_PARTICIPANTS",
    "CHOSEN_MATCH",
    "CHOSEN_ROUND",
    "ADD_MATCH_RESULT",
    "FIND_TOURNAMENT_BY_NAME",
    "FIND_TOURNAMENT_BY_LIST_ONGOING",
    "FIND_TOURNAMENT_BY_LIST_FUTURE",
    "FIND_TOURNAMENT_BY_LIST_PAST",
    "FIND_TOURNAMENT_BY_LIST_ALL",
])

RequestAnswer: TypeAlias = Request | tuple[Request, list[object]]
