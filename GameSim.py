import random
import sys

from Game import Game
from Timer import Timer


class GameSim:
    def __init__(self, player_number, game_id):
        self.id = game_id
        self.game = Game()
        self.answers = []
        self.cards = self.game.cards
        self.player_number = player_number
        self.player_hands = [[] for _ in range(player_number)]
        self.player_shows = self.player_hands.copy()
        self.guess_number = 0
        self.total_runtime = 0
        self.output_print = True
        self.game.evaluate_values = [1, 3, 3, 27, 12, 12]

    def setup(self):
        game = self.game

        cards = list(game.cards.keys())

        self.gen_answers()
        for card in self.answers:
            cards.remove(card)

        player_hand_sizes = [0 for _ in range(self.player_number)]

        i = 0
        for _ in range(len(game.cards) - 3):
            new_card = self.random_card(cards)
            self.player_hands[i].append(new_card)
            player_hand_sizes[i] += 1
            cards.remove(new_card)
            i = (i + 1) % self.player_number

        for player in range(self.player_number):
            game.add_player(f"{player}", player_hand_sizes[player])

        game.your_player_hand = self.player_hands[0]
        game.your_player = game.players[0]

        game.update_position()

    def run(self):
        p = self.print
        total_timer = Timer(f"{self.id}")
        p("--------------------------------------")
        p("--PREGAME INFO--")
        for i, hand in enumerate(self.player_hands):
            p(f"Hand of player {i + 1}: {hand}")
        p(f"GEN ANSWERS: {self.answers}")
        p()
        timer = Timer(f"{self.id}-guess")
        while not self.game.check_confirmed():
            original_score = self.game.position.evaluate()
            timer.reset()
            guesses = self.game.determine_guesses()
            timer.stop()
            try:
                guess = list(guesses.keys())[0]
            except IndexError:
                print(self.answers)
                for hand in self.player_hands:
                    print(hand)
                sys.exit()
            check = self.check_show(guess)
            self.game.add_guess([0, check[0], check[1], guess])
            new_score = self.game.position.evaluate()

            p()
            p(f"--GUESS {self.guess_number + 1}--")
            p(f"Total outcome count: {self.game.outcome_count}")
            p(f"Time to generate guesses: {timer.runtime} s")
            p(f"Guesses generated: {len(guesses)}")
            p(f"Top guesses: {list(guesses.items())}")
            p(f"Cards: {guess}")
            p(f"Return: {check}")
            p(f"Score: {new_score - original_score}")

            self.guess_number += 1

        p()
        p("--GAME INFO--")
        for i, hand in enumerate(self.player_hands):
            p(f"Hand of player {i}: {hand}")
        p(f"GEN ANSWERS: {self.answers}")
        p(f"CONFIRMED CHARACTER: {self.game.position.confirmed_character}")
        p(f"CONFIRMED ROOM: {self.game.position.confirmed_room}")
        p(f"CONFIRMED WEAPON: {self.game.position.confirmed_weapon}")
        p(f"AMOUNT OF GUESSES: {self.guess_number}")
        p(f"RUNTIME: {total_timer.stop()} s")
        self.total_runtime = total_timer.runtime
        p("--------------------------------------")

    def gen_answers(self):
        sorted_cards = {"CHARACTER": [], "ROOM": [], "WEAPON": []}
        for card, card_type in self.game.cards.items():
            sorted_cards[card_type].append(card)

        char_answer = self.random_card(sorted_cards["CHARACTER"])
        room_answer = self.random_card(sorted_cards["ROOM"])
        weapon_answer = self.random_card(sorted_cards["WEAPON"])

        self.answers += [char_answer, room_answer, weapon_answer]

    def check_show(self, guess):
        for i, hand in enumerate(self.player_hands):
            if i == 0:
                continue
            show_card = None
            for card in guess:
                if card in self.player_shows[i]:
                    show_card = card
                    return i, show_card
                elif card in hand:
                    show_card = card

            if show_card:
                print(show_card)
                self.player_shows[i].append(show_card)
                return i, show_card

        return None, None

    def print(self, string=""):
        if self.output_print:
            print(string)

    @staticmethod
    def random_card(card_list):
        return card_list[random.randint(0, len(card_list) - 1)]