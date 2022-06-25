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
    def __init__(self, answers, player_number, id):
        self.id = id
        self.game = Game()
        self.answers = answers
        self.player_number = player_number
        self.player_hands = [[] for _ in range(player_number)]
        self.guess_number = 0
        self.setup()

    def setup(self):
        game = self.game

        cards = list(game.cards.keys())
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

    def random_card(self, card_list):
        card = card_list[random.randint(0, len(card_list) - 1)]
        return card

    def check_show(self, guess):
        for i, player in enumerate(self.player_hands):
            if i == 0:
                continue
            for card in guess:
                if card in player:
                    return i, card

        return None, None

    def run(self):
        print("--------------------------------------")
        for i, hand in enumerate(self.player_hands):
            print(f"Hand of player {i + 1}: {hand}")
        print(f"GEN ANSWERS: {self.answers}")
        print()
        timer = Timer(f"{self.id}")
        while not self.game.check_confirmed():
            self.guess_number += 1
            timer.reset()
            guesses = self.game.determine_guesses()
            timer.stop()
            guess = list(guesses.keys())[0]
            check = self.check_show(guess)
            self.game.add_guess(Guess(0, check[0], check[1], guess))

            print(f"GUESS NUMBER {self.guess_number}")
            print(f"Cards: {guess}")
            print(f"Return: {check}")
            print(f"Time to generate guesses: {timer.runtime}")

        for i, hand in enumerate(self.player_hands):
            print(f"Hand of player {i}: {hand}")
        print(f"GEN ANSWERS: {self.answers}")
        print(f"CONFIRMED CHARARCTER: {self.game.position.confirmed_character}")
        print(f"CONFIRMED ROOM: {self.game.position.confirmed_room}")
        print(f"CONFIRMED WEAPON: {self.game.position.confirmed_weapon}")
        print(f"AMOUNT OF GUESSES: {self.guess_number}")
        print("--------------------------------------")
