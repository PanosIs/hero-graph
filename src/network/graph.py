import numpy
from sklearn.preprocessing import normalize

class Draft_Graph_Network:
    def __init__(self, hero_pool_size : int, learning_rate : float):
        self.connections = numpy.full(shape=(hero_pool_size, hero_pool_size), fill_value=0.5)
        numpy.fill_diagonal(self.connections, val=0)

        self.learning_rate = learning_rate

    def train_single_example(self, picks : list, win : bool):
        nonzero = numpy.outer(picks, picks)
        numpy.fill_diagonal(nonzero, val=0)
        if(not win):
            nonzero *= -1
        self.connections += self.learning_rate * nonzero

    def get_connections(self):
        return self.connections

