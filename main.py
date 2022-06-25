import sys
from Game import Game
from Guess import Guess
from Timer import Timer
from GameSim import GameSim
from GameGen import GameGen

game_sim = GameSim(4, 0)
game_sim.run()
# game_gen = GameGen(50)
sys.exit()


# PLAYER AMOUNT GREATLY INCREASES RUNTIME

game = Game()
game.add_player("Zander", 5)
game.add_player("Father", 5)
game.add_player("Mother", 4)
game.add_player("Aly", 4)
game.your_player_hand += ["MRS WHITE", "KITCHEN", "MR GREEN", "ROPE", "STUDY"]
your_player = game.players[0]
game.your_player = your_player
game.start()
game.add_guess(Guess(0, 2, "LEAD PIPE", ["STUDY", "COLONEL MUSTARD", "LEAD PIPE"]))

guess_timer = Timer("guess")
guesses = game.determine_guesses()
print(guess_timer.stop())
print(len(guesses))
goo_goo = list(guesses.items())
print(goo_goo)

# GUESS (KITCHEN, PROFESSOR PLUM, REVOLVER) says average score of 10.0 but should be 0
# bc we know revolver is in the hand right next to us.
