from python_ne.core.backend_adapters.backend_adapter import BackendAdapter
from python_ne.core.backend_adapters.default_dense_layer_adapter import DefaultDenseLayerAdapter
from python_ne.core.neural_network import activations
from python_ne.core.neural_network.dense_layer import DenseLayer
from python_ne.core.neural_network.neural_network import NeuralNetwork


class DefaultBackendAdapter(BackendAdapter):
    def add_dense_layer(self, **kwargs):
        if kwargs['activation'] == 'sigmoid':
            kwargs['activation'] = activations.sigmoid
        else:
            raise Exception(f'activation function {kwargs["activation"]} is not valid')

        self.model.add(DenseLayer(**kwargs))

    def build_model(self):
        return NeuralNetwork()

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights()

    def predict(self, obs):
        return self.model.predict(obs)

    def get_layers(self):
        return [DefaultDenseLayerAdapter(layer) for layer in self.model.layers]
