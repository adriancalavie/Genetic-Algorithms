import operator
from random import choice, uniform, randint
import matplotlib.pyplot as plt
from pip._vendor.distlib.compat import raw_input

mutation_rate = 0.02

# Motors are characterised by power and weight
motors = {
    '000': (2., 3.),
    '001': (4., 3.5),
    '010': (6., 4.),
    '011': (7., 5.),
    '100': (8., 4.5),
    '101': (10., 5.),
    '110': (12., 6.),
    '111': (14., 7.5),
}

# Motors are characterised by range and weight
batteries = {
    '000': (3., 5.),
    '001': (6., 6.5),
    '010': (9., 7.),
    '011': (10., 7.),
    '100': (12., 7.5),
    '101': (15., 8.),
    '110': (18., 10.),
    '111': (21., 12.5),
}


def show_generations(history):
    """
    Prints the population throughout history.
    """
    plots = []

    parameters = {
        'font.size': 7,
        'axes.titlesize': 12,
        'toolbar': 'None'
    }
    plt.rcParams.update(parameters)
    plt.get_current_fig_manager().full_screen_toggle()  # toggle fullscreen mode

    for i in range(10):
        index, row = 0, 0
        if i < 5:
            index = i
            row = 0
        else:
            index = i - 5
            row = 1
        plot = plt.subplot2grid((2, 5), (row, index))
        plots.append(plot)

    for i, gen in enumerate(history):
        plot = plots[i]
        plot.set_title('Generation {0}'.format(i + 1))
        plot.set_xlabel('Fitness')
        # noinspection PyTypeChecker
        gen = dict(sorted(gen.items(), key=operator.itemgetter(1)))
        plot.barh(list(gen.keys()), gen.values())
    plt.draw()
    plt.waitforbuttonpress(0)  # this will wait for indefinite time
    plt.close()


def get_fitness(chromosome):
    """
    This is the fitness function. It calculates the value for a specific chromosome using the formula:

    Fitness = Range + Power - Weight

    :param chromosome: bitstring
    :return: a positive value
    """
    motor_power, motor_weight = motors[chromosome[:3]]
    battery_range, battery_weight = batteries[chromosome[3:]]

    fitness = battery_range + motor_power - (motor_weight + battery_weight)

    return fitness if fitness >= 0. else 0


def mutate(offspring):
    offspring_as_list = list(offspring)
    for i in range(len(offspring_as_list)):
        random_chance = uniform(0., 1.)
        if random_chance <= mutation_rate:
            offspring_as_list[i] = '0' if offspring_as_list[i] == '1' else '1'

    return ''.join(offspring_as_list)


def crossover(parents):
    """
    Does the DNA-like crossover for a pair of parents.
    :param parents: bitstring tuple
    :return: the children and their fitness score
    """
    parent1, parent2 = parents
    index = randint(1, len(parent1) - 1)

    first_part1 = parent1[:index]
    second_part1 = parent2[:index]

    first_part2 = parent1[index:]
    second_part2 = parent2[index:]

    first_child = first_part1 + second_part2
    second_child = second_part1 + first_part2

    mutate(first_child)
    mutate(second_child)

    return (first_child, get_fitness(first_child)), (second_child, get_fitness(second_child))


def init_population():
    """
    Initializes a population of 16 robots.
    :return: the population as a dict()
    """
    population = {}

    while len(population) < 16:
        first_gene = choice(list(motors.keys()))
        second_gene = choice(list(batteries.keys()))
        parent = first_gene + second_gene
        population[parent] = get_fitness(parent)

    return population


def get_new_generation(population):
    """
    Generates a new population.
    :return: a dict() representing the new population.
    """
    kids = {}

    while len(kids) < len(population):
        parent1 = roulette(population)

        candidate = roulette(population)
        while candidate == parent1:
            candidate = roulette(population)

        parent2 = candidate

        kid1, kid2 = crossover((parent1, parent2))

        if kid1 == kid2:
            print("Same kids")
            exit(1)

        kids[kid1[0]] = kid1[1]
        kids[kid2[0]] = kid2[1]

    return kids


def roulette(population):
    """
    This is a selection function. It selects one individual based on it's fitness score: the bigger the score,
    the bigger the chance it gets to breed.
    """
    fitness = list(population.values())
    individuals = list(population.keys())
    fit_sum = sum(fitness)

    pivot = uniform(0, fit_sum)

    current = fitness[0]
    index = 0

    while current < pivot:
        index += 1
        current += fitness[index]

    return individuals[index]


def run():
    current_gen = init_population()
    history = list(dict())
    for i in range(10):
        # print('Generation {0}:'.format(i + 1))
        # print('Population is: ', current_gen)
        history.append(current_gen)
        current_gen = get_new_generation(current_gen)

        # if input('do you want to show generations? ') in ('yes', 'Y', 'Yes'):
    show_generations(history)

    # plt.plot([sum(gen.values()) for gen in history])
    # plt.show()
    

if __name__ == '__main__':
    run()
