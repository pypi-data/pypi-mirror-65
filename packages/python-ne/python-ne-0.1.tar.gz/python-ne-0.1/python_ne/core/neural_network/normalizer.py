def normalize(x_list):
    return [(x - min(x_list)) / (max(x_list) - min(x_list)) for x in x_list]
