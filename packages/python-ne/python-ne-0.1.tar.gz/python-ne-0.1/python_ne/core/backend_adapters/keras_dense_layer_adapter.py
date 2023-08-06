from python_ne.core.backend_adapters.dense_layer_adapter import DenseLayerAdapter


class KerasDenseLayerAdapter(DenseLayerAdapter):
    def get_units(self):
        return self.layer.units

    def get_activation(self):
        return self.layer.activation

    def get_weights(self):
        return self.layer.get_weights()

    def set_weights(self, weights):
        self.layer.set_weights(weights)

    def get_input_shape(self):
        return self.layer.input_shape[1],
