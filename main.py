from Game import Game
from Guess import Guess
from Timer import Timer


game = Game()
game.add_player("Zander", 5)
game.add_player("Father", 5)
game.add_player("Mother", 4)
game.add_player("Aly", 4)
your_player = game.players[0]
game.your_player = your_player
game.update_position()
game.position.players[0].reveal_card("BILLIARD ROOM")
game.position.players[0].reveal_card("COLONEL MUSTARD")
game.position.players[0].reveal_card("MISS SCARLET")
game.position.players[0].reveal_card("ROPE")
game.position.players[0].reveal_card("WRENCH")
game.position.players[0].possible_cards = {}
game.position.add_guess(Guess(0, 2, "MRS PEACOCK", ["BILLIARD ROOM", "MRS PEACOCK", "ROPE"]))
game.position.add_guess(Guess(0, 1, "REVOLVER", ["BILLIARD ROOM", "MISS SCARLET", "REVOLVER"]))
game.position.add_guess(Guess(0, 3, "KNIFE", ["BILLIARD ROOM", "MISS SCARLET", "KNIFE"]))
game.position.add_guess(Guess(0, 2, "STUDY", ["STUDY", "MISS SCARLET", "WRENCH"]))
game.position.add_guess(Guess(0, None, None, ["LOUNGE", "MISS SCARLET", "ROPE"]))

guess_timer = Timer("guess")
guesses = game.determine_guesses()
print(guess_timer.stop())
print(len(guesses))
goo_goo = [item for item in guesses.items()]
for i in range(len(goo_goo)):
    print(goo_goo[i])

# GUESS (KITCHEN, PROFESSOR PLUM, REVOLVER) says average score of 10.0 but should be 0
# bc we know revolver is in the hand right next to us.
