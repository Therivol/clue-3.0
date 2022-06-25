from GameSim import GameSim


class GameGen:
    def __init__(self, number):
        runtimes = []
        guesses = []
        instances = 0
        for i in range(number):
            game_sim = GameSim(4, i)
            game_sim.output_print = False
            game_sim.run()
            guesses.append(game_sim.guess_number)
            runtimes.append(game_sim.total_runtime)
            print(f"Game {i + 1} - {game_sim.guess_number} guesses")

            instances += 1

        average_runtime = sum(runtimes) / instances
        average_guesses = sum(guesses) / instances
        print()
        print(f"AVERAGE RUNTIME: {average_runtime}")
        print(f"AVERAGE GUESSES: {average_guesses}")



