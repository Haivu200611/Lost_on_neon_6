class Inventory:
    def __init__(self):
        self.items = {}

    def add(self,item):
        self.items[item] = self.items.get(item,0)+1