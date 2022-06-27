import sys
from Game import Game
from Timer import Timer
from GameSim import GameSim
from GameGen import GameGen
from GameLearn import GameLearn

# game_gen = GameGen(1000, 3)

game = Game()
game.add_player("Zander", 6)
game.add_player("Father", 6)
game.add_player("Aly", 6)
game.your_player_hand = ['MRS PEACOCK', 'MISS SCARLET', 'BILLIARD ROOM', 'KITCHEN', 'HALL', 'BALLROOM']
game.your_player = game.players[0]
game.start()
game.add_guess([0, 1, "STUDY", ['STUDY', 'COLONEL MUSTARD', 'REVOLVER']])

print(game.determine_guesses())

# game_sim = GameSim(3, 0)
# game_sim.run()
# game_gen = GameGen(500, 3)

# test = GameLearn(300, 3, [1, 3, 3, 27, 12, 12], 3, 3)

# PLAYER AMOUNT GREATLY INCREASES RUNTIME
