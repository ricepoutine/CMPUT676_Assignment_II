class Item(object):
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.cost = value/weight
        self.accept = 0