import random
from Game import Game
from Guess import Guess
from Timer import Timer


class GameGen:
    def __init__(self):
        games = {}

    def generate_cards(self, cards):
        characters = [x for x in cards if cards[x].type == "CHARACTER"]
        rooms = [x for x in cards if cards[x].type == "ROOM"]
        weapons = [x for x in cards if cards[x].type == "WEAPON"]

        character_answer = characters[random.randint(0, len(characters))]
        room_answer = rooms[random.randint(0, len(rooms))]
        weapon_answer = weapons[random.randint(0, len(weapons))]


class GameSim:
    def __init__(self, player_number, id):
        self.id = id
        self.game = Game()
        self.answers = []
        self.cards = self.game.cards
        self.player_number = player_number
        self.player_hands = [[] for _ in range(player_number)]
        self.player_shows = self.player_hands.copy()
        self.guess_number = 0
        self.setup()

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

    def gen_answers(self):
        characters = [card.name for card in self.cards.values() if card.type == "CHARACTER"]
        rooms = [card.name for card in self.cards.values() if card.type == "ROOM"]
        weapons = [card.name for card in self.cards.values() if card.type == "WEAPON"]

        char_answer = self.random_card(characters)
        room_answer = self.random_card(rooms)
        weapon_answer = self.random_card(weapons)

        self.answers += [char_answer, room_answer, weapon_answer]

    def random_card(self, card_list):
        card = card_list[random.randint(0, len(card_list) - 1)]
        return card

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

    def run(self):
        print("--------------------------------------")
        print("--PREGAME INFO--")
        for i, hand in enumerate(self.player_hands):
            print(f"Hand of player {i + 1}: {hand}")
        print(f"GEN ANSWERS: {self.answers}")
        print()
        total_timer = Timer(f"{self.id}")
        timer = Timer(f"{self.id}-guess")
        while not self.game.check_confirmed():
            original_score = self.game.position.evaluate()
            timer.reset()
            guesses = self.game.determine_guesses()
            timer.stop()
            guess = list(guesses.keys())[0]
            # KEY ERROR SOMETIMES IDK :(
            check = self.check_show(guess)
            self.game.add_guess(Guess(0, check[0], check[1], guess))
            new_score = self.game.position.evaluate()

            print()
            print(f"--GUESS {self.guess_number + 1}--")
            print(f"Outcome count: {self.game.outcome_count}")
            print(f"Time to generate guesses: {timer.runtime} s")
            print(f"Cards: {guess}")
            print(f"Return: {check}")
            print(f"Score: {new_score - original_score}")

            self.guess_number += 1

        print()
        print("--GAME INFO--")
        for i, hand in enumerate(self.player_hands):
            print(f"Hand of player {i}: {hand}")
        print(f"GEN ANSWERS: {self.answers}")
        print(f"CONFIRMED CHARARCTER: {self.game.position.confirmed_character}")
        print(f"CONFIRMED ROOM: {self.game.position.confirmed_room}")
        print(f"CONFIRMED WEAPON: {self.game.position.confirmed_weapon}")
        print(f"AMOUNT OF GUESSES: {self.guess_number}")
        print(f"TOTAL RUNTIME: {total_timer.stop()} s")
        print("--------------------------------------")
