from Player import Player


class Position:
    def __init__(self, game):
        self.game = game
        self.possible_cards = game.cards.copy()
        self.cards = game.cards.copy()
        self.confirmed_character = None
        self.confirmed_room = None
        self.confirmed_weapon = None

        self.cur_stack = []
        self.next_stack = []

        self.players = [Player(self, player[0], player[1]) for player in game.players]
        for card in game.your_player_hand:
            self.add_command(self.players[0].reveal_card, card, True)

        self.update_info()

        for guess in game.guesses:
            self.add_guess(guess)

    def add_command(self, command, arg, immediate=False):
        if immediate:
            self.cur_stack.append([command, arg])
        else:
            self.next_stack.append([command, arg])

    def update_info(self):
        while len(self.cur_stack) > 0:
            command, arg = self.cur_stack[0]
            command(arg)
            self.cur_stack.pop(0)

        if len(self.next_stack) > 0:
            self.cur_stack = self.next_stack.copy()
            self.next_stack.clear()
            self.update_info()

    def eliminate_card(self, card):
        self.possible_cards.pop(card, None)

    def confirm_card(self, card, card_type):
        # print(f"CONFIRMED {card}")
        if card_type == "WEAPON":
            self.confirmed_weapon = card
        elif card_type == "CHARACTER":
            self.confirmed_character = card
        elif card_type == "ROOM":
            self.confirmed_room = card

        self.possible_cards = {n: c for n, c in self.possible_cards.items() if c != card_type}

    def add_guess(self, guess):
        if guess[1]:
            i = (guess[0] + 1) % self.game.player_number
            while i != guess[1]:
                for card in guess[3]:
                    self.add_command(self.players[i].eliminate_card, card, True)
                i = (i + 1) % self.game.player_number

            if guess[2]:
                self.add_command(self.players[i].reveal_card, guess[2], True)
            else:
                self.add_command(self.players[i].add_show_set, guess[3], True)

        else:
            for player in self.players:
                for card in guess[3]:
                    self.add_command(player.eliminate_card, card, True)

        self.update_info()

    def evaluae(self):
        vals = self.game.evaluate_values

        score = 0
        for player in self.players:
            score -= vals[0] * len(player.possible_cards)
            score += vals[1] * len(player.known_cards)
        score -= vals[2] * len(self.possible_cards)
        if self.confirmed_character:
            score += vals[3]
        if self.confirmed_room:
            score += vals[4]
        if self.confirmed_weapon:
            score += vals[5]
        return score

    def evaluate_outcome(self, guess):
        confirmed = self.confirmed_character, self.confirmed_room, self.confirmed_weapon
        possible_cards = self.possible_cards.copy()
        player_info = []
        for player in self.players:
            info = player.possible_cards.copy(), player.known_cards.copy(), player.show_sets.copy()
            player_info.append(info)

        self.add_guess(guess)
        score = self.evaluate()

        self.confirmed_character, self.confirmed_room, self.confirmed_weapon = confirmed
        self.possible_cards = possible_cards
        for i, player in enumerate(self.players):
            info = player_info[i]
            player.possible_cards, player.known_cards, player.show_sets = info

        return score

    def print_info(self):
        print("-----------------------------------------")
        print("GAME INFO: ")
        print(f"Confirmed character: {self.confirmed_character}")
        print(f"Confirmed room: {self.confirmed_room}")
        print(f"Confirmed weapon: {self.confirmed_weapon}")
        print(f"Possible cards({len(self.possible_cards)}): {list(self.possible_cards.keys())}")
        print()
        print("PLAYER INFO: ")
        for player in self.players:
            print(f"--{player.name}--")
            print(f"Known cards({len(player.known_cards)}): {list(player.known_cards.keys())}")
            print(f"Possible cards({len(player.possible_cards)}): {list(player.possible_cards.keys())}")

        print("-----------------------------------------")
        print()

    def evaluate(self):
        p_val, g_val = self.game.p_val, self.game.g_val
        c_num, r_num, w_num = self.game.character_number - 1, self.game.room_number - 1, self.game.weapon_number - 1
        card_values = {"ROOM": c_num / r_num, "CHARACTER": c_num / r_num, "WEAPON": w_num / r_num}

        score = 0
        for player in self.players:
            for card_type in player.possible_cards.values():
                score -= p_val * card_values[card_type]
        for card_type in self.possible_cards.values():
            score -= g_val * card_values[card_type]
        if self.confirmed_character:
            score += 27 * c_num
        if self.confirmed_room:
            score += 27 * r_num
        if self.confirmed_weapon:
            score += 27 * w_num
        return score
