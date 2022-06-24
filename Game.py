from Player import Player
from Position import Position
from Card import Card
from Guess import Guess


class Game:
    def __init__(self):
        self.players = []
        self.your_player = None

        self.cards = {}
        self.load_cards()

        self.guesses = []
        self.position = None
        self.score = 0

        self.player_number = len(self.players)
        self.card_number = len(self.cards)
        self.character_number = len([card for card in self.cards.values() if card.type == "CHARACTER"])
        self.room_number = len([card for card in self.cards.values() if card.type == "ROOM"])
        self.weapon_number = len([card for card in self.cards.values() if card.type == "WEAPON"])

        self.p_val = 1
        self.g_val = self.p_val * (self.player_number - 1)

        self.update_position()
        self.play_game()

    def play_game(self):
        pass

    def update_position(self):
        self.position = Position(self)
        self.score = self.position.evaluate()

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

    def determine_guesses(self):
        guesses = self.generate_guesses()
        outcomes = {}
        for guess in guesses:
            average_score = 0
            score_total = 0
            outcome_iter = 0
            for outcome in self.get_outcomes(guess):
                eval = outcome.evaluate() - self.score
                score_total += eval
                outcome_iter += 1

            if outcome_iter == 0:
                print(guess)
                outcome_iter = 1
            average_score = score_total / outcome_iter
            outcomes[tuple(guess)] = round(average_score, 2)

        outcomes = dict(sorted(outcomes.items(), key=lambda x: x[1], reverse=True))
        return outcomes

    def generate_guesses(self):
        guesses = []

        characters = [card.name for card in self.cards.values() if card.type == "CHARACTER"]
        rooms = [card.name for card in self.cards.values() if card.type == "ROOM"]
        weapons = [card.name for card in self.cards.values() if card.type == "WEAPON"]

        for character in characters:
            for room in rooms:
                for weapon in weapons:
                    cards = [character, room, weapon]
                    prune = True
                    for card in cards:
                        known = False
                        if not self.position.possible_cards.get(card):
                            known = True
                        if not known:
                            prune = False
                            break

                    if prune:
                        continue

                    guesses.append([room, character, weapon])

        return guesses

    def get_outcomes(self, guess):
        outcomes = []
        your_player_index = 0
        for i, player in enumerate(self.position.players):
            if i == your_player_index:
                continue
            player_outcomes = []
            has_to_have = False
            for card in guess:
                if player.known_cards.get(card):
                    has_to_have = True
                    outcome = Position(self)
                    outcome.add_guess(Guess(your_player_index, i, card, guess))
                    outcomes.append(outcome)
                elif player.possible_cards.get(card):
                    outcome = Position(self)
                    outcome.add_guess(Guess(your_player_index, i, card, guess))
                    player_outcomes.append(outcome)
                if has_to_have:
                    return outcomes

            outcomes += player_outcomes

        last_outcome = Position(self)
        last_outcome.add_guess(Guess(your_player_index, None, None, guess))
        outcomes.append(last_outcome)
        return outcomes

    def add_player(self, name, hand_size):
        self.players.append([name, hand_size])
        self.player_number += 1
        self.g_val = self.p_val * (self.player_number - 1)
        self.update_position()
