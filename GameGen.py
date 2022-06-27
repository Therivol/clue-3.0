import random

from GameSim import GameSim


class GameGen:
    def __init__(self, iterations, player_number=None, values=None):
        self.values = values
        self.average_guesses = 0
        runtimes = []
        guesses = []
        instances = 0
        if not player_number:
            player_number = random.randint(3, 6)
        for i in range(iterations):
            game_sim = GameSim(player_number, i)
            if values:
                game_sim.game.evaluate_values = values
            game_sim.setup()
            game_sim.output_print = False
            game_sim.run()
            guesses.append(game_sim.guess_number)
            runtimes.append(game_sim.total_runtime)
            print(f"Game {i + 1} - {game_sim.guess_number} guesses")

            instances += 1

        average_runtime = sum(runtimes) / instances
        average_guesses = sum(guesses) / instances
        self.average_guesses = average_guesses
        accuracies = [abs(number - average_guesses) for number in guesses]
        average_accuracy = sum(accuracies) / instances
        print()
        print(f"AVERAGE RUNTIME: {round(average_runtime, 4)}")
        print(f"AVERAGE GUESSES: {average_guesses}")
        print(f"AVERAGE ACCURACY: +/-{round(average_accuracy, 4)}")



