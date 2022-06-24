from Player import Player


class Position:
    def __init__(self, game):
        self.game = game
        self.cards = game.cards
        self.possible_cards = game.cards.copy()
        self.players = []
        self.confirmed_character = None
        self.confirmed_room = None
        self.confirmed_weapon = None

        for player in game.players:
            self.players.append(Player(self, player[0], player[1]))

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
        for player in self.players:
            score -= self.game.p_val * len(player.possible_cards)
            score += self.game.g_val * len(player.known_cards)
        score -= self.game.g_val * len(self.possible_cards)
        if self.confirmed_character:
            score += self.game.g_val * (self.game.character_number - 1)
        if self.confirmed_room:
            score += self.game.g_val * (self.game.room_number - 1)
        if self.confirmed_weapon:
            score += self.game.g_val * (self.game.weapon_number - 1)
        return score
