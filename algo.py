import random


class Knapsack:
    MAX_WEIGHT = 200
    INIT_POPULATION_SIZE = 100
    CROSSOVER_POINTS = 2
    MUTATE_CHANCE = 10
    GENERATIONS = 1000

    def __init__(self, items: list) -> None:
        self.items = items
        self.chromosome_length = len(self.items)
        self.solve_log = []

    def solve(self) -> list:
        init_population = self.get_init_population()

        for iter in range(self.GENERATIONS):
            parent1, parent2 = self.select_parents(init_population)
            
            child = self.crossover(parent1, parent2)

            self.mutate(child)

            self.local_improvement(child)

            init_population.append(child)
            self.remove_worst_individual(init_population)

            self.solve_log.append((iter, self.evaluate_individual(self.get_best_individual(init_population))[1]))

        return self.evaluate_individual(self.get_best_individual(init_population))

    def get_init_population(self) -> list:
        popultion = [[0 for _ in range(self.chromosome_length)] for _ in range(self.INIT_POPULATION_SIZE)]

        for individual in popultion:
            individual[random.randint(0, self.chromosome_length-1)] = 1

        return popultion
    
    def get_best_individual(self, population: list) -> int:
        best_individual = population[0]
        
        for individual in population:
            if self.evaluate_individual(individual)[1] > self.evaluate_individual(best_individual)[1]:
                best_individual = individual

        return best_individual

    def remove_worst_individual(self, population: list) -> None:
        worst_individual = population[0]

        for individual in population:
            if self.evaluate_individual(individual)[1] < self.evaluate_individual(worst_individual)[1]:
                worst_individual = individual

        population.remove(worst_individual)

    def select_parents(self, population: list) -> list:
        return self.get_best_individual(population), random.choice(population)

    def crossover(self, parent1: list, parent2: list) -> list:
        points = sorted([random.randint(0, self.chromosome_length-1) for _ in range(self.CROSSOVER_POINTS)])
        child = []
        parent = parent1
        last_point = 0

        for point in points:
            child += parent[last_point:point]

            parent = parent1 if parent == parent2 else parent2

            last_point = point

        child += parent[last_point:]

        return child if self.evaluate_individual(child)[0] <= self.MAX_WEIGHT else parent
    
    def mutate(self, individual: list) -> None:
        if random.randint(1, self.MUTATE_CHANCE) == 1:
            gen_number = random.randint(0, self.chromosome_length-1)

            self.toggle_gen(individual, gen_number)

            if self.evaluate_individual(individual)[0] > self.MAX_WEIGHT:
                self.toggle_gen(individual, gen_number)
    
    def evaluate_individual(self, individual: list) -> int:
        weight = 0
        value = 0
        
        for gen_number in range(self.chromosome_length):
            if individual[gen_number] == 1:
                weight += self.items[gen_number][0]
                value += self.items[gen_number][1]

        return weight, value            

    def local_improvement(self, individual: list) -> None:
        evaluation = self.evaluate_individual(individual)
        best_evaluation = evaluation[1] - evaluation[0]
        best_gen_number = -1

        for gen_number in range(self.chromosome_length):
            self.toggle_gen(individual, gen_number)

            evaluation = self.evaluate_individual(individual)
            current_evalutaion = evaluation[1] - evaluation[0]

            if evaluation[0] <= self.MAX_WEIGHT and current_evalutaion > best_evaluation:
                best_evaluation = current_evalutaion
                best_gen_number = gen_number
            
            self.toggle_gen(individual, gen_number)

        if best_gen_number != -1:
            self.toggle_gen(individual, best_gen_number)

    def toggle_gen(self, individual: list, gen_number: int) -> None:
        individual[gen_number] = 1 if individual[gen_number] == 0 else 0