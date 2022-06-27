from Position import Position


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
        self.character_number = len([ct for ct in self.cards.values() if ct == "CHARACTER"])
        self.room_number = len([ct for ct in self.cards.values() if ct == "ROOM"])
        self.weapon_number = len([ct for ct in self.cards.values() if ct == "WEAPON"])

        self.evaluate_values = []
        self.p_val = 1
        self.g_val = self.p_val * (len(self.players) - 1)

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
        evaluate = self.position.evaluate_outcome
        for guess in guesses:
            score_total = 0
            outcome_iter = 0
            guess_outcomes = get_outcomes(guess)
            if len(guess_outcomes) == 1:
                continue
            for outcome in guess_outcomes:
                evaluation = evaluate(outcome) - self.score
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

        sorted_cards = {"CHARACTER": [], "ROOM": [], "WEAPON": []}
        for card, card_type in self.cards.items():
            sorted_cards[card_type].append(card)

        for room in sorted_cards["ROOM"]:
            for character in sorted_cards["CHARACTER"]:
                for weapon in sorted_cards["WEAPON"]:
                    cards = [room, character, weapon]
                    prune = not any(True for card in cards if card in self.position.possible_cards)
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
                    outcomes.append([your_player_index, i, card, guess])
                elif player.possible_cards.get(card):
                    player_outcomes.append([your_player_index, i, card, guess])
                if has_to_have:
                    return outcomes

            outcomes += player_outcomes

        outcomes.append([your_player_index, None, None, guess])

        return outcomes

    def check_confirmed(self):
        c = self.position.confirmed_character
        r = self.position.confirmed_room
        w = self.position.confirmed_weapon

        return c and r and w

    def add_player(self, name, hand_size):
        self.players.append([name, hand_size])
        self.player_number += 1
        # self.g_val = self.p_val * (self.player_number - 1)
        self.update_position()

    def load_cards(self):
        self.cards["REVOLVER"] = "WEAPON"
        self.cards["KNIFE"] = "WEAPON"
        self.cards["LEAD PIPE"] = "WEAPON"
        self.cards["ROPE"] = "WEAPON"
        self.cards["CANDLESTICK"] = "WEAPON"
        self.cards["WRENCH"] = "WEAPON"

        self.cards["MRS PEACOCK"] = "CHARACTER"
        self.cards["MISS SCARLET"] = "CHARACTER"
        self.cards["COLONEL MUSTARD"] = "CHARACTER"
        self.cards["MR GREEN"] = "CHARACTER"
        self.cards["PROFESSOR PLUM"] = "CHARACTER"
        self.cards["MRS WHITE"] = "CHARACTER"

        self.cards["BILLIARD ROOM"] = "ROOM"
        self.cards["STUDY"] = "ROOM"
        self.cards["HALL"] = "ROOM"
        self.cards["LOUNGE"] = "ROOM"
        self.cards["DINING ROOM"] = "ROOM"
        self.cards["BALLROOM"] = "ROOM"
        self.cards["CONSERVATORY"] = "ROOM"
        self.cards["LIBRARY"] = "ROOM"
        self.cards["KITCHEN"] = "ROOM"