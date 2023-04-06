import questionary as q
from ..requests import Request, RequestAnswer
from ..validators import *
from .common import clear_screen_and_show_log, print_title, print_list_title, print_important_info

class TournamentsMenus:

    @clear_screen_and_show_log
    def show_manage_tournaments_menu(self):
        print_title("Tournaments menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Register a new tournament", value=Request.ADD_TOURNAMENT),
                q.Choice(title="Manage existing tournament", value=Request.EDIT_TOURNAMENT),
                q.Choice(title="List tournaments", value=Request.LIST_TOURNAMENTS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MAIN_MENU)])
        return question.ask()

    @clear_screen_and_show_log
    def show_manage_unready_tournament_menu(self, tournament_info):
        print_title("Unready tournament menu")
        print_important_info(f"{tournament_info['str']}")
        choice_start_tournament = q.Choice(title=f"Start tournament", value=Request.GENERATE_MATCHES)
        if tournament_info["total_participants"] < 2:
            choice_start_tournament.disabled = "Not enough participants"
        elif tournament_info["total_participants"] % 2 == 1:
            choice_start_tournament.disabled = "Select an even number of participants"
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title=f"Manage participants ({tournament_info['total_participants']})", value=Request.MANAGE_PARTICIPANTS),
                choice_start_tournament,
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if not answer:
            return Request.MANAGE_TOURNAMENT
        return answer

    @clear_screen_and_show_log
    def show_manage_tournament_menu(self, tournament_info):
        print_title("Tournament menu")
        print_important_info(f"{tournament_info['str']}")

        #print(f"selected tournament : {tournament_info['str']}")
        #print(f"{tournament_info['total_started_rounds']=}")
        # print(f"{tournament_info['total_matches']=}")
        # print(f'{tournament_info["total_finished_matches"]=}')
        #print(f'{tournament_info["is_current_round_started"]=}')
        #print(f'{tournament_info["name"]=}, {tournament_info["location"]=}, {tournament_info["begin_date"]=},'
        #      f'{tournament_info["end_date"]=}, {tournament_info["total_rounds"]=}, {tournament_info["total_started_rounds"]=},'
        #      f'{tournament_info["total_finished_matches"]=}, {tournament_info["total_matches"]=}',
        #      f'{tournament_info["total_finished_rounds"]=}, {tournament_info["total_participants"]=}')

        choices = []
        if tournament_info["total_finished_rounds"] < tournament_info["total_rounds"]:
            print_important_info(
                f"{tournament_info['current_round_name']} ({tournament_info['total_started_rounds']}/{tournament_info['total_rounds']})")
            if not tournament_info["is_current_round_started"]:
                choice_register_or_start_round = q.Choice(title="Start the round", value=Request.START_ROUND)
            else:
                choice_register_or_start_round = q.Choice(title="Register a match score",
                                                          value=Request.REGISTER_MATCH_SCORE)
            choices.extend([
                choice_register_or_start_round,
                q.Separator(),
                q.Choice(title="List matches of the current round", value=Request.LIST_MATCHES)])
        else:
            print_important_info("Tournament Ended")

        choices.extend([
            q.Choice(title="List all rounds matches (and scores)", value=Request.LIST_ROUNDS_SCORES),
            q.Choice(title="List participants", value=Request.LIST_PARTICIPANTS),
            q.Separator(),
            q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])

        question = q.select(
            "What do you want to do ?", choices=choices)
        return question.ask()

    @clear_screen_and_show_log
    def keep_or_change_tournament(self, last_edited_tournament):
        print_title("Tournament selection menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title=f"Keep editing {last_edited_tournament}", value=Request.KEEP_SELECTED_TOURNAMENT),
                q.Choice(title="Select a new one", value=Request.CHANGE_SELECTED_TOURNAMENT),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    @clear_screen_and_show_log
    def show_tournament_registration(self) -> RequestAnswer:
        print_title("Tournament registration menu")
        add_tournament_questions = [
            {
                "type": "text", "name": "name", "qmark": ">",
                "message": "Enter Tournament name :",
                "validate": lambda x: len(x.strip()) > 0
            },
            {
                "type": "text", "name": "location", "qmark": ">",
                "message": "Enter location :",
                "validate": non_empty_alphabet_validator
            },
            {
                "type": "text", "name": "begin_date", "qmark": ">",
                "message": "Enter begin date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {
                "type": "text", "name": "end_date", "qmark": ">",
                "message": "Enter end date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {"type": "text", "name": "total_rounds", "qmark": ">",
             "message": "Total number of rounds :",
             "validate": lambda x: x.isnumeric(),
             "default": "4"}
        ]
        raw_tournament_data = q.prompt(add_tournament_questions)
        if not raw_tournament_data:  # ctrl-c
            return Request.MANAGE_TOURNAMENT, None
        else:
            return Request.REGISTER_TOURNAMENT_DATA, raw_tournament_data

    @clear_screen_and_show_log
    def how_to_choose_tournament(self, statistics) -> RequestAnswer:
        print_title("Tournament selection method menu")
        question = q.select(
            "Which tournament do you want to manage ?",
            choices=[
                q.Choice(title="Find by name", value=Request.FIND_TOURNAMENT_BY_NAME),
                q.Choice(title=f"Find from list of ongoing tournaments ({statistics['ongoing']})", value=Request.FIND_TOURNAMENT_BY_LIST_ONGOING),
                q.Choice(title=f"Find from list of future tournaments ({statistics['future']})", value=Request.FIND_TOURNAMENT_BY_LIST_FUTURE),
                q.Choice(title=f"Find from list of past tournaments ({statistics['past']})", value=Request.FIND_TOURNAMENT_BY_LIST_PAST),
                q.Choice(title=f"Find from list of all tournaments ({statistics['all']})", value=Request.FIND_TOURNAMENT_BY_LIST_ALL),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    @clear_screen_and_show_log
    def choose_tournament_by_name(self, tournaments_info):
        print_title("Tournament selection menu")
        tournaments_meta = {f"{t_index}- {tournament_name}": tournament_str
                            for t_index, tournament_name, tournament_str in tournaments_info}
        question = q.autocomplete(
            "Enter the tournament name :",
            choices=list(tournaments_meta.keys()), meta_information=tournaments_meta,
            validate=lambda x: x in list(tournaments_meta.keys()))
        answer = question.ask()
        if answer is None:
            return Request.MANAGE_TOURNAMENT, None
        else:
            selected_tournament = int(answer.partition("-")[0])
            return Request.SELECTED_TOURNAMENT, selected_tournament

    @clear_screen_and_show_log
    def choose_tournament_by_list(self, tournaments_info):
        print_title("Tournament selection menu")
        choices = [q.Choice(title=tournament_name, value=t_index) for t_index, tournament_name, _ in tournaments_info]
        choices.extend([q.Separator(), q.Choice("Back")])
        question = q.select(
            "Select a tournament: ",
            choices=choices)
        answer = question.ask()
        if answer is None or answer is "Back":
            return Request.MANAGE_TOURNAMENT, None
        else:
            return Request.SELECTED_TOURNAMENT, answer

    @clear_screen_and_show_log
    def show_list_tournaments_menu(self, total_tournaments):
        # some kind repetitive code with player list. to-do: refactor ?
        print_title("Tournaments list menu")
        q.print(f">> Total {total_tournaments} tournaments")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Print list", value=Request.PRINT_TOURNAMENTS),
                q.Choice(title="Export list", value=Request.EXPORT_TOURNAMENTS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    @clear_screen_and_show_log
    def print_tournaments(self, tournaments_info):
        print_list_title("Tournaments list")
        for tournament_info in tournaments_info:
            q.print(tournament_info)
        back_choice = q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)
        question = q.select(
            "",
            choices=[
                back_choice,
                q.Choice(title="Export this list", value=Request.EXPORT_TOURNAMENTS)],
            default=back_choice)
        answer = question.ask()
        if not answer:
            return Request.MANAGE_TOURNAMENT
        return answer
