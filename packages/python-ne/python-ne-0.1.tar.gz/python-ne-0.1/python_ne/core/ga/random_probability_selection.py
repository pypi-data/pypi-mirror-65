import random


class ListElement:
    def __init__(self, probability, data):
        self.data = data
        self.probability = probability


class RandomProbabilitySelection:

    def __init__(self):
        self.elements = []

    def perform_selection(self, number_to_be_selected):
        self.elements.sort(key=lambda element: element.probability)

        selected_elements = []

        for _ in range(number_to_be_selected):
            random_number = random.random()
            probability_sum = 0
            for element in self.elements:
                probability_sum += element.probability
                if random_number <= probability_sum and element not in selected_elements:
                    selected_elements.append(element)
                    break

        return [selected_element.data for selected_element in selected_elements]

    def add_element(self, data, probability):
        self.elements.append(ListElement(probability=probability, data=data))

    def add_elements(self, elements):
        for element in elements:
            self.add_element(data=element['data'], probability=element['probability'])
