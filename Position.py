from Player import Player


class Position:
    def __init__(self, game):
        self.game = game
        self.cards = game.cards
        self.possible_cards = game.cards.copy()
        self.confirmed_character = None
        self.confirmed_room = None
        self.confirmed_weapon = None

        self.players = [Player(self, player[0], player[1]) for player in game.players]
        for card in game.your_player_hand:
            self.players[0].reveal_card(card)

        for guess in game.guesses:
            self.add_guess(guess)

    def eliminate_card(self, *args):
        for card in args:
            self.possible_cards.pop(card, None)

    def eliminate_from_others(self, player, card):
        for other in self.players:
            if other == player:
                continue
            other.eliminate_card(card)

    def confirm_card(self, card):
        # print(f"CONFIRMED {card}")
        card_type = self.cards[card].type
        if card_type == "WEAPON":
            self.confirmed_weapon = card
        elif card_type == "CHARACTER":
            self.confirmed_character = card
        elif card_type == "ROOM":
            self.confirmed_room = card

        self.possible_cards = {n: c for n, c in self.possible_cards.items() if c.type != card_type}

    def add_guess(self, guess):
        if guess.show_player_pos:
            i = (guess.guess_player_pos + 1) % self.game.player_number
            while i != guess.show_player_pos:
                for card in guess.cards:
                    self.players[i].eliminate_card(card)
                i = (i + 1) % self.game.player_number

            if guess.show_card:
                self.players[i].reveal_card(guess.show_card)
            else:
                self.players[i].add_show_set(guess.cards)

        else:
            for player in self.players:
                for card in guess.cards:
                    player.eliminate_card(card)

    def evaluate(self):
        score = 0
        p_val, g_val = self.game.p_val, self.game.g_val
        for player in self.players:
            score -= p_val * len(player.possible_cards) / 2
            score += g_val * len(player.known_cards)
        score -= self.game.g_val * len(self.possible_cards)
        if self.confirmed_character:
            score += g_val * (self.game.character_number - 1)
        if self.confirmed_room:
            score += g_val * (self.game.room_number - 1)
        if self.confirmed_weapon:
            score += g_val * (self.game.weapon_number - 1)
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
