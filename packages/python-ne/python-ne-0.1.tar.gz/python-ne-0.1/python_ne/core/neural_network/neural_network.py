class NeuralNetwork:

    def __init__(self):
        self.layers = []

    def predict(self, x_list):
        output = None
        for index, layer in enumerate(self.layers):
            layer.input_shape = x_list.shape if index == 0 else output.shape
            layer.initialize()
            output = layer.feedforward(x_list if index == 0 else output)

        return output

    def add(self, layer):
        self.layers.append(layer)
