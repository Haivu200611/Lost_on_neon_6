from settings import RESOURCE_KEYS


class Inventory:
    def __init__(self):
        self.items = {key: 0 for key in RESOURCE_KEYS}

    def add(self, item: str, amount: int = 1) -> None:
        if item not in self.items:
            return
        self.items[item] += amount

    def get(self, item: str) -> int:
        return self.items.get(item, 0)

    def can_afford(self, cost: dict[str, int]) -> bool:
        for key, amount in cost.items():
            if self.get(key) < amount:
                return False
        return True

    def spend(self, cost: dict[str, int]) -> bool:
        if not self.can_afford(cost):
            return False
        for key, amount in cost.items():
            self.items[key] -= amount
        return True
