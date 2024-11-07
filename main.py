import random
from algo import Knapsack


ITEM_COUNT = 100
MIN_ITEM_VALUE = 2
MAX_ITEM_VALUE = 20
MIN_ITEM_WEIGHT = 1
MAX_ITEM_WEIGHT = 10

def generate_random_items() -> list:
    items = []
    
    for _ in range(ITEM_COUNT):
        item_weight = random.randint(MIN_ITEM_WEIGHT, MAX_ITEM_WEIGHT)
        item_value = random.randint(MIN_ITEM_VALUE, MAX_ITEM_VALUE)

        items.append((item_weight, item_value))

    return items


if __name__ == '__main__':
    items = generate_random_items()
    
    print("Weights:", list(map(lambda x: x[0], items)))
    print("Values:", list(map(lambda x: x[1], items)))

    result = Knapsack(items).solve()

    print(f"Value: {result[0][1]}")
    print(result[1])