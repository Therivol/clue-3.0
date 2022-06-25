import sys

from Game import Game
from Guess import Guess
from Timer import Timer
from GameGen import GameSim

game = GameSim(4, 0)
game.run()
sys.exit()

game = Game()
game.add_player("Zander", 5)
game.add_player("Father", 5)
game.add_player("Mother", 4)
game.add_player("Aly", 4)
game.your_player_hand += ["MRS WHITE", "KITCHEN", "MR GREEN", "KNIFE", "STUDY"]
your_player = game.players[0]
game.your_player = your_player
game.start()
game.add_guess(Guess(0, 2, "BILLIARD ROOM", ["BILLIARD ROOM", "MRS PEACOCK", "REVOLVER"]))
game.add_guess(Guess(0, 1, "HALL", ["HALL", "MRS PEACOCK", "REVOLVER"]))

guess_timer = Timer("guess")
guesses = game.determine_guesses()
print(guess_timer.stop())
print(len(guesses))
goo_goo = [item for item in guesses.items()]
for i in range(20):
    pass
    print(goo_goo[i])

# GUESS (KITCHEN, PROFESSOR PLUM, REVOLVER) says average score of 10.0 but should be 0
# bc we know revolver is in the hand right next to us.
