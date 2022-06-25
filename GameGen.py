import random

from GameSim import GameSim


class GameGen:
    def __init__(self, number):
        runtimes = []
        guesses = []
        instances = 0
        for i in range(number):
            game_sim = GameSim(random.randint(3, 6), i)
            game_sim.output_print = False
            game_sim.run()
            guesses.append(game_sim.guess_number)
            runtimes.append(game_sim.total_runtime)
            print(f"Game {i + 1} - {game_sim.guess_number} guesses")

            instances += 1

        average_runtime = sum(runtimes) / instances
        average_guesses = sum(guesses) / instances
        accuracies = [abs(number - average_guesses) for number in guesses]
        average_accuracy = sum(accuracies) / instances
        print()
        print(f"AVERAGE RUNTIME: {round(average_runtime, 4)}")
        print(f"AVERAGE GUESSES: {average_guesses}")
        print(f"AVERAGE ACCURACY: +/-{round(average_accuracy, 4)}")



