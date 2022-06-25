from Position import Position
from Card import Card
from Guess import Guess


class Game:
    def __init__(self):
        self.players = []
        self.your_player = None
        self.your_player_hand = []

        self.cards = {}
        self.load_cards()

        self.guesses = []
        self.position = None
        self.score = 0
        self.outcome_count = 0

        self.player_number = len(self.players)
        self.card_number = len(self.cards)
        self.character_number = len([card for card in self.cards.values() if card.type == "CHARACTER"])
        self.room_number = len([card for card in self.cards.values() if card.type == "ROOM"])
        self.weapon_number = len([card for card in self.cards.values() if card.type == "WEAPON"])

        self.p_val = 1
        self.g_val = self.p_val * (self.player_number - 1)

    def start(self):
        self.update_position()

    def update_position(self):
        self.position = Position(self)
        self.score = self.position.evaluate()

    def add_guess(self, guess):
        self.guesses.append(guess)
        self.update_position()

    def determine_guesses(self):
        # print(f"Current pos score: {self.score}")
        guesses = self.generate_guesses()
        outcomes = {}
        outcome_count = 0
        get_outcomes = self.get_outcomes
        for guess in guesses:
            score_total = 0
            outcome_iter = 0
            guess_outcomes = get_outcomes(guess)
            if len(guess_outcomes) == 1:
                pass
                # print(guess, guess_outcomes)
            for outcome in guess_outcomes:
                evaluation = outcome - self.score
                score_total += evaluation
                outcome_iter += 1

            outcome_count += outcome_iter
            average_score = score_total / outcome_iter
            outcomes[tuple(guess)] = round(average_score, 2)

        outcomes = dict(sorted(outcomes.items(), key=lambda x: x[1], reverse=True))
        self.outcome_count = outcome_count

        return outcomes

    def generate_guesses(self):
        guesses = []

        characters = [card.name for card in self.cards.values() if card.type == "CHARACTER"]
        rooms = [card.name for card in self.cards.values() if card.type == "ROOM"]
        weapons = [card.name for card in self.cards.values() if card.type == "WEAPON"]

        for character in characters:
            for room in rooms:
                for weapon in weapons:
                    cards = [room, character, weapon]
                    prune = not any(self.position.possible_cards.get(card) for card in cards)
                    if prune:
                        continue

                    guesses.append(cards)

        return guesses

    def get_outcomes(self, guess):
        outcomes = []
        your_player_index = 0
        position = self.position
        for i, player in enumerate(self.position.players):
            if i == your_player_index:
                continue
            player_outcomes = []
            has_to_have = False
            for card in guess:
                if player.known_cards.get(card):
                    has_to_have = True
                    outcomes.append(position.evaluate_outcome(Guess(your_player_index, i, card, guess)))
                elif player.possible_cards.get(card):
                    player_outcomes.append(position.evaluate_outcome(Guess(your_player_index, i, card, guess)))
                if has_to_have:
                    return outcomes

            outcomes += player_outcomes

        outcomes.append(position.evaluate_outcome(Guess(your_player_index, None, None, guess)))

        return outcomes

    def check_confirmed(self):
        c = self.position.confirmed_character
        r = self.position.confirmed_room
        w = self.position.confirmed_weapon

        return c and r and w

    def add_player(self, name, hand_size):
        self.players.append([name, hand_size])
        self.player_number += 1
        self.g_val = self.p_val * (self.player_number - 1)
        self.update_position()

    def load_cards(self):
        self.cards["REVOLVER"] = (Card("REVOLVER", "WEAPON"))
        self.cards["KNIFE"] = (Card("KNIFE", "WEAPON"))
        self.cards["LEAD PIPE"] = (Card("LEAD PIPE", "WEAPON"))
        self.cards["ROPE"] = (Card("ROPE", "WEAPON"))
        self.cards["CANDLESTICK"] = (Card("CANDLESTICK", "WEAPON"))
        self.cards["WRENCH"] = (Card("WRENCH", "WEAPON"))

        self.cards["MRS PEACOCK"] = (Card("MRS PEACOCK", "CHARACTER"))
        self.cards["MISS SCARLET"] = (Card("MISS SCARLET", "CHARACTER"))
        self.cards["COLONEL MUSTARD"] = (Card("COLONEL MUSTARD", "CHARACTER"))
        self.cards["MR GREEN"] = (Card("MR GREEN", "CHARACTER"))
        self.cards["MRS WHITE"] = (Card("MRS WHITE", "CHARACTER"))
        self.cards["PROFESSOR PLUM"] = (Card("PROFESSOR PLUM", "CHARACTER"))

        self.cards["BILLIARD ROOM"] = (Card("BILLIARD ROOM", "ROOM"))
        self.cards["STUDY"] = (Card("STUDY", "ROOM"))
        self.cards["HALL"] = (Card("HALL", "ROOM"))
        self.cards["LOUNGE"] = (Card("LOUNGE", "ROOM"))
        self.cards["DINING ROOM"] = (Card("DINING ROOM", "ROOM"))
        self.cards["BALLROOM"] = (Card("BALLROOM", "ROOM"))
        self.cards["CONSERVATORY"] = (Card("CONSERVATORY", "ROOM"))
        self.cards["LIBRARY"] = (Card("LIBRARY", "ROOM"))
        self.cards["KITCHEN"] = (Card("KITCHEN", "ROOM"))
