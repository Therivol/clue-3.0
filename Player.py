
class Player:
    def __init__(self, position, name, hand_size):
        self.position = position
        self.name = name
        self.hand_size = hand_size
        self.possible_cards = position.cards.copy()
        self.known_cards = {}
        self.show_sets = []
        self.queue = []

    def eliminate_card(self, card):
        position = self.position
        possible_cards = self.possible_cards

        possible_cards.pop(card, None)

        for show_set in self.show_sets:
            show_set.pop(card, None)
            if len(show_set) == 1:
                position.add_command(self.reveal_card, show_set[0])

        confirm_card = True
        for player in position.players:
            if card in player.possible_cards or card in player.known_cards:
                confirm_card = False
        if confirm_card:
            position.confirm_card(card, position.cards[card])

        if self.hand_size - len(self.known_cards) == len(possible_cards):
            for card in possible_cards.copy():
                position.add_command(self.reveal_card, card)

    def reveal_card(self, card):
        position = self.position
        known_cards = self.known_cards
        possible_cards = self.possible_cards
        show_sets = self.show_sets

        possible_cards.pop(card, None)
        known_cards[card] = position.cards[card]
        position.eliminate_card(card)

        show_sets = [show for show in show_sets if card not in show]

        self.eliminate_from_others(card)

        if len(known_cards) == self.hand_size:
            for card in possible_cards:
                position.add_command(self.eliminate_card, card)

    def add_show_set(self, cards):
        if any(True for card in cards if card in self.known_cards):
            return

        all_cards = self.position.cards
        possible_cards = self.possible_cards

        show = {card: all_cards[card] for card in cards if card in possible_cards}

        len_show = len(show)
        if len_show > 1:
            self.show_sets.append(show)

        elif len_show == 1:
            self.position.add_command(self.reveal_card, show[0])

    def eliminate_from_others(self, card):
        position = self.position
        for player in position.players:
            if player is self:
                continue
            position.add_command(player.eliminate_card, card)
