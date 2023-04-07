import questionary as q
from ..requests import Request, RequestAnswer
from .common import clear_screen_and_show_log, print_title


class MatchesMenus:
    @clear_screen_and_show_log
    def show_matches(self, matches):
        print_title("Matches list")
        for match in matches:
            print(match)

    @clear_screen_and_show_log
    def select_match(self, matches_info) -> RequestAnswer:
        print_title("Match selection menu")
        # print(matches_info)
        question = q.select("Which match ?", choices=matches_info)
        #   q.Separator(),
        #   q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if answer:
            return Request.SELECTED_MATCH, matches_info.index(answer)
        else:
            return Request.MANAGE_TOURNAMENT, None

    @clear_screen_and_show_log
    def enter_score(self, players) -> RequestAnswer:
        print_title("Score registration menu")
        question = q.select(
            "Select the result of the match, for the first player",
            choices=[
                q.Choice(title=f"{players[0]}: WIN  - {players[1]}: LOSE ", value="WIN"),
                q.Choice(title=f"{players[0]}: LOSE - {players[1]}: WIN ", value="LOSE"),
                q.Choice(title="DRAW", value="DRAW"),
            ],
        )
        answer = question.ask()
        if answer:
            return Request.ADD_MATCH_RESULT, answer
        else:
            return Request.MANAGE_TOURNAMENT, None
