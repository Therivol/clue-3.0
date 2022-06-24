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
game.position.add_guess(Guess(0, 3, "KNIFE", ["BILLIARD ROOM", "KNIFE", "MR GREEN"]))
#game.position.add_guess(Guess(0, 2, "STUDY", ["STUDY", "MR GREEN", "KNIFE"]))
#game.position.add_guess(Guess(0, 1, "HALL", ["HALL", "MR GREEN", "KNIFE"]))
#game.position.add_guess(Guess(0, 3, "KNIFE", ["LOUNGE", "MR GREEN", "KNIFE"]))

guess_timer = Timer("guess")
guesses = game.determine_guesses()
print(guess_timer.stop())
print(len(guesses))
goo_goo = [item for item in guesses.items()]
for i in range(10):
    print(goo_goo[i])
