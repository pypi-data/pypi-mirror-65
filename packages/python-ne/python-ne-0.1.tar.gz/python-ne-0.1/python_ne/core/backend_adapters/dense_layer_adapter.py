class DenseLayerAdapter:

    def __init__(self, layer):
        self.layer = layer

    def get_units(self):
        raise NotImplementedError()

    def get_activation(self):
        raise NotImplementedError()

    def get_weights(self):
        raise NotImplementedError()

    def set_weights(self, weights):
        raise NotImplementedError()

    def get_input_shape(self):
        raise NotImplementedError()
