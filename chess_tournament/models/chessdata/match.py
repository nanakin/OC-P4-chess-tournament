from dataclasses import dataclass
from enum import Enum
from typing import Tuple
from .participant import Participant
from ..serialization import Serializable


@dataclass
class Match(Serializable):
    """Round's match data."""

    class Points(Enum):
        WIN = 1.0
        LOSE = 0.0
        DRAW = 0.5

    participants_pair: Tuple[Participant, Participant]
    participants_scores: Tuple[Points, Points] | None = None

    def __str__(self):
        player_1, player_2 = (
            self.participants_pair[0].player,
            self.participants_pair[1].player,
        )
        score_player_1, score_player_2 = (
            (self.participants_scores[0].name, self.participants_scores[1].name)
            if self.participants_scores is not None
            else ("", "")
        )
        return f"{player_1} {score_player_1}".ljust(39) + "vs" + f"{player_2} {score_player_2}".rjust(39)

    @property
    def is_ended(self):
        return self.participants_scores is not None

    @classmethod
    def get_pairs_score_from_first(cls, first_result):
        if first_result == cls.Points.WIN:
            return cls.Points.WIN, cls.Points.LOSE
        if first_result == cls.Points.LOSE:
            return cls.Points.LOSE, cls.Points.WIN
        return cls.Points.DRAW, cls.Points.DRAW

    def register_score(self, participants_status: Tuple[Points, Points]):
        self.participants_scores = participants_status
        for participant, score in zip(self.participants_pair, self.participants_scores):
            participant.add_score(score.value)

    def encode(self):
        return {
            "participants_pair": [participant.encode() for participant in self.participants_pair],
            "participants_scores": [score.name for score in self.participants_scores] if self.is_ended else [],
        }

    @classmethod
    def decode(cls, encoded_data):
        encoded_data["participants_scores"] = (
            tuple([cls.Points[encoded_score] for encoded_score in encoded_data["participants_scores"]])
            if encoded_data["participants_scores"]
            else None
        )
        encoded_data["participants_pair"] = tuple(
            [Participant.decode(encoded_participant) for encoded_participant in encoded_data["participants_pair"]]
        )

        return cls(**encoded_data)
