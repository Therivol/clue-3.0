from GameGen import GameGen
import random


class GameLearn:
    def __init__(self, iterations, player_number, base_values, child_number, depth):
        self.iterations = iterations
        self.player_number = player_number
        self.base_values = base_values
        self.child_number = child_number
        self.depth = depth
        self.last_winner = None
        self.last_winner = GameGen(iterations,  player_number, base_values)

        self.new_generation(base_values, depth)

    def new_generation(self, values, depth):
        if self.depth == 0:
            return
        children = []
        if self.last_winner:
            children.append(self.last_winner)
        for i in range(self.child_number):
            modified_values = self.modify_values(values)
            child = GameGen(self.iterations, self.player_number, modified_values)
            print(f"{child.average_guesses}")
            print(f"{child.values}")
            children.append(child)

        children = sorted(children, key=lambda x: x.average_guesses)
        new_gen_base = children[0]
        self.last_winner = new_gen_base
        values = new_gen_base.values
        self.print_info(new_gen_base, depth)
        self.new_generation(values, depth - 1)

    @staticmethod
    def modify_values(values):
        new_values = []
        for value in values:
            if random.randint(1, 4) == 1:
                mod = random.randint(1, 3) / 3
                if random.randint(0, 1) == 0:
                    new_values.append(value + mod)
                else:
                    new_values.append(value - mod)
            else:
                new_values.append(value)
        return new_values

    def print_info(self, game_gen, depth):
        print(f"-------------------------------")
        print(f"GENERATION {self.depth - depth}")
        print(f"Average Guesses: {game_gen.average_guesses}")
        print(f"Values: {game_gen.values}")
        print(f"-------------------------------")
