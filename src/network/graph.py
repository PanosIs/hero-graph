import numpy
from src.utils.data_utils import get_match_dataset
from sklearn.preprocessing import normalize

numpy.set_printoptions(threshold=numpy.nan, precision=2, suppress = True)

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
        return self.connections / self.connections.max()


def train_graph_net():
    data = get_match_dataset()
    for input, target in data:
        radiant = input[0:116]
        dire = input[116:232]
        n.train_single_example(radiant, target)
        n.train_single_example(dire, not target)


n = Draft_Graph_Network(116, 0.1)
train_graph_net()
a = n.get_connections()
print(numpy.where(a == a.max()))