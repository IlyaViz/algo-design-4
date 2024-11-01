from matplotlib import pyplot as plt
from main import generate_random_items
from algo import Knapsack


if __name__ == "__main__":
    items = generate_random_items()
    knapsack = Knapsack(generate_random_items())
    knapsack.solve()

    iters = [sl[0] for sl in knapsack.solve_log]
    values = [sl[1] for sl in knapsack.solve_log]

    print(knapsack.solve_log)

    plt.plot(iters, values)

    plt.xlabel("Iterations")
    plt.ylabel("Target function value")

    plt.show()