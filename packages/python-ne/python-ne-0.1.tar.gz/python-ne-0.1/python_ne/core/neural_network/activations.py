import math


def sigmoid(value):
    return 1 / (1 + math.e ** -value)
