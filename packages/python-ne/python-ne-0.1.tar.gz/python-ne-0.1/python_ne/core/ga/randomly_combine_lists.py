import random
import numpy as np


def get_list_parts(list_x):
    mid_index = len(list_x) // 2
    return [list_x[:mid_index], list_x[mid_index:]]


def random_pop(list_x):
    return list_x.pop(random.randrange(len(list_x)))


def get_random_lists_combinations(l1, l2, return_shape):
    if len(l1) == 1:
        return l2.reshape(return_shape), l1.reshape(return_shape)

    l1_parts = get_list_parts(l1)
    l2_parts = get_list_parts(l2)

    return (
        np.array([*random_pop(l1_parts), *random_pop(l2_parts)]).reshape(return_shape),
        np.array([*random_pop(l2_parts), *random_pop(l1_parts)]).reshape(return_shape)
    )
