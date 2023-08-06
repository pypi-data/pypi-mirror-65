from keras.engine.saving import load_model

from python_ne.core.ga_neural_network.neat_neural_network import NeatNeuralNetwork


def save_element(element, file_path):
    element.model.save(file_path)


def load_element(file_path, output_size, input_shape):
    model = load_model(file_path)
    element = NeatNeuralNetwork(create_model=False, output_size=output_size, input_shape=input_shape)
    element.model = model
    return element
