

class Player:
    def __init__(self, position, name, hand_size):
        self.position = position
        self.name = name
        self.hand_size = hand_size
        self.possible_cards = position.cards.copy()
        self.known_cards = {}
        self.show_sets = []

    def eliminate_card(self, card):
        self.possible_cards.pop(card, None)

        for show_set in self.show_sets:
            show_set.pop(card, None)
            if len(show_set) == 1:
                self.reveal_card(show_set[0])

        confirm_card = True
        for player in self.position.players:
            if player.possible_cards.get(card) or player.known_cards.get(card):
                confirm_card = False

        if confirm_card:
            self.position.confirm_card(card)

        if self.hand_size - len(self.known_cards) == len(self.possible_cards):
            possible_cards_temp = self.possible_cards.copy()
            for card in possible_cards_temp:
                self.reveal_card(card)

    def reveal_card(self, card):
        self.position.eliminate_card(card)
        self.known_cards[card] = self.position.cards[card]
        self.possible_cards.pop(card, None)

        if len(self.known_cards) == self.hand_size:
            self.possible_cards.clear()

        self.position.eliminate_from_others(self, card)

        for i, show in enumerate(self.show_sets):
            if show.get(card):
                self.show_sets.pop(i)

    def add_show_set(self, cards):
        for card in cards:
            if self.known_cards.get(card):
                return

        show = {card: self.position.cards[card] for card in cards if self.possible_cards.get(card)}

        if len(show) > 1:
            self.show_sets.append(show)

        elif len(show) == 1:
            self.reveal_card(show[0])
