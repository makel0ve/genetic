import random


def initialize_population(matrix, population_size, start_node):
    population = []
    nodes = []
    for i in range(0, len(matrix)):
        if i != start_node:
            nodes.append(i)
    
    for _ in range(population_size):
        individual = [start_node] + random.sample(nodes, len(nodes))
        population.append(individual)
        
    return population


def calculate_fitness(individual, matrix):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += matrix[individual[i]][individual[i + 1]]
    total_distance += matrix[individual[-1]][individual[0]]

    return 1 / total_distance


def select_parents(population, fitness):
    total_fitness = sum(fitness)
    probabilities = [f / total_fitness for f in fitness]
    parents = random.choices(population, weights=probabilities, k=2)
    
    return parents


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2))
    
    child1 = [None] * size
    child2 = [None] * size
    
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]
    
    def fill_child(child, parent):
        for i in range(size):
            if child[i] is None:
                for node in parent:
                    if node not in child:
                        child[i] = node
                        break
        
        return child
    
    return fill_child(child1, parent2), fill_child(child2, parent1)


def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(1, len(individual)), 2))
        individual[start:end] = reversed(individual[start:end])
    
    return individual


def create_new_generation(population, matrix, mutation_rate):
    fitness = [calculate_fitness(individual, matrix) for individual in population]
    elite_size = int(0.1 * len(population))
    
    sorted_population = sorted(population, key=lambda ind: calculate_fitness(ind, matrix), reverse=True)
    new_population = sorted_population[:elite_size]
    
    while len(new_population) < len(population):
        parent1, parent2 = select_parents(population, fitness)
        child1, child2 = crossover(parent1, parent2)
        
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        
        new_population.append(child1)
        if len(new_population) < len(population):
            new_population.append(child2)
    
    return new_population


def genetic_algorithm(matrix, population_size, max_generations_without_improvement, mutation_rate, start_node):
    population = initialize_population(matrix, population_size, start_node)
    
    best_distance = 10**6
    best_solution = None
    generations_without_improvement = 0
    generations_score = 0
    
    while generations_without_improvement < max_generations_without_improvement:
        population = create_new_generation(population, matrix, mutation_rate)
        best_individual = max(population, key=lambda ind: calculate_fitness(ind, matrix))
        best_individual_distance = 1 / calculate_fitness(best_individual, matrix)
        
        if best_individual_distance < best_distance:
            best_distance = best_individual_distance
            best_solution = best_individual
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        generations_score += 1
        
    
    return best_solution, best_distance, generations_score
    

def main():
    print("Введите путь до файла с матрицей смежности.")
    file = input().strip().replace('"', '')
    f = open(file, 'r')
    matrix = []
    for line in f:
        matrix.append(list(map(int, line.split())))

    print("Введите количество популяций. Рекомендуется вести в диапазоне 50-200.")
    population_size = int(input())
    print("Введите условие остановки алгоритма. Число поколений без улучшений результата.")
    max_generations_without_improvement = int(input())
    print("Введите вероятность мутации.")
    mutation_rate = float(input())
    print(f"Введите начало маршрута (0-{len(matrix)}).")
    start_node = int(input())
    

    solution, distance, generations_score = genetic_algorithm(matrix, population_size, max_generations_without_improvement, mutation_rate, start_node)
    solution.append(solution[0])
    print(f"Кратчайший маршрут:\n{', '.join(map(str, solution))}")
    print(f"Длина кратчайшего маршрута:\n{round(distance, 2)}")
    print(f"Количество поколений:\n{generations_score-max_generations_without_improvement}")
    

if __name__ == "__main__":
    main()
    