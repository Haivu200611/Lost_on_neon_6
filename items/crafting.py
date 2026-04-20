RECIPES = {
    "oxygen_tank": {"iron":3}
}

def craft(inv,item):
    if item not in RECIPES:
        return False

    for r in RECIPES[item]:
        if inv.items.get(r,0) < RECIPES[item][r]:
            return False

    for r in RECIPES[item]:
        inv.items[r] -= RECIPES[item][r]

    inv.add(item)
    return True