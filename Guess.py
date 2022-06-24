from dataclasses import dataclass


@dataclass
class Guess:
    guess_player_pos: any
    show_player_pos: any
    show_card: any
    cards: list[any]


class Accusation:
    pass
