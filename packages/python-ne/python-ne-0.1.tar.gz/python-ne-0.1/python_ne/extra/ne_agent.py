import numpy as np

from python_ne.core.ga.genetic_algorithm import GeneticAlgorithm
from python_ne.core.neural_network import normalizer
# from python_ne.core.saving import save_element, load_element


class NeAgent:

    def __init__(self, env_adapter, selection_percentage, mutation_chance, input_shape, population_size,
                 fitness_threshold):
        self.env_adapter = env_adapter
        self.output_size = self.env_adapter.get_n_actions()
        self.input_shape = input_shape
        self.best_element = None

        self.genetic_algorithm = GeneticAlgorithm(
            population_size=population_size,
            input_shape=self.input_shape,
            output_size=self.output_size,
            selection_percentage=selection_percentage,
            mutation_chance=mutation_chance,
            fitness_threshold=fitness_threshold,
            ne_type='ne',  # ne or neat
            backend_adapter='default',  # default or keras,
            neural_network_config=[128, 128]  # two hidden layers with 128 neurons each
        )

    def train(self, number_of_generations):
        self.genetic_algorithm.run(
            number_of_generations=number_of_generations,
            calculate_fitness_callback=self.calculate_fitness
        )

        self.best_element = self.genetic_algorithm.get_best_element()

    def calculate_fitness(self, element):
        return self.play(element)

    # def save(self, file_path):
    #     save_element(element=self.best_element, file_path=file_path)
    #
    # def load(self, file_path):
    #     self.best_element = load_element(
    #         file_path=file_path,
    #         output_size=self.output_size,
    #         input_shape=self.input_shape
    #     )

    def play(self, element=None):
        element = self.best_element if element is None else element
        self.env_adapter.reset()
        done = False
        observation, _, _ = self.env_adapter.step(self.env_adapter.get_random_action())
        fitness = 0
        while not done:
            observation = normalizer.normalize(observation)
            action = element.get_output(np.array(observation))
            observation, reward, done = self.env_adapter.step(action)
            fitness += reward if reward > 0 else 0
        return fitness
