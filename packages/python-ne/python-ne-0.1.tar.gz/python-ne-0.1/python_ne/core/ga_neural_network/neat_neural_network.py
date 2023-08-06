import random
import numpy as np

from python_ne.core.ga_neural_network.ga_neural_network import GaNeuralNetwork
from python_ne.core.neural_network import activations
from python_ne.core.neural_network.dense_layer import DenseLayer
from python_ne.core.neural_network.neural_network import NeuralNetwork

number_of_neurons_choices = [16, 32, 64, 128, 256, 512, 1024]


class NeatNeuralNetwork(GaNeuralNetwork):

    def __init__(self, topology=None, *args, **kwargs):
        self.topology = self.create_topology() if topology is None else topology
        super(NeatNeuralNetwork, self).__init__(*args, **kwargs)

    def create_topology(self):
        hidden_layers_count = random.randint(2, 8)
        return [random.choice(number_of_neurons_choices) for _ in range(hidden_layers_count)]

    def create_model(self):
        model = self.backend_adapter()

        for i, units in enumerate(self.topology):
            if i == 0:
                model.add_dense_layer(units=units, input_shape=self.input_shape, activation=activations.sigmoid)
            else:
                model.add_dense_layer(units=units, activation=activations.sigmoid)

        model.add_dense_layer(units=self.output_size, activation=activations.sigmoid)

        return model

    def get_output(self, obs):
        return np.argmax(self.model.predict(obs))

    def crossover(self, other):
        child1 = NeatNeuralNetwork(
            input_shape=self.input_shape,
            output_size=self.output_size,
            topology=[*self.topology[:len(self.topology) // 2], *other.topology[len(other.topology) // 2:]],
            backend_adapter=self.backend_adapter,
            neural_network_config=self.neural_network_config
        )

        child2 = NeatNeuralNetwork(
            input_shape=self.input_shape,
            output_size=self.output_size,
            topology=[*other.topology[:len(other.topology) // 2], *self.topology[len(self.topology) // 2:]],
            backend_adapter=self.backend_adapter,
            neural_network_config=self.neural_network_config
        )
        return child1, child2

    def mutate(self):
        for layer in self.model.get_layers():
            weights = layer.get_weights()[0]
            bias = layer.get_weights()[1]

            prev_layer_neuron_count, current_layer_neuron_count = weights.shape

            for prev_neuron in range(prev_layer_neuron_count):
                for cur_neuron in range(current_layer_neuron_count):
                    if random.random() < 0.1:
                        weights[prev_neuron][cur_neuron] = random.uniform(-1, 1)

            for i in range(len(bias)):
                if random.random() < 0.1:
                    bias[i] = random.uniform(-1, 1)

            layer.set_weights((weights, bias))

    def __str__(self):
        return f'fitness = {self.fitness}'
