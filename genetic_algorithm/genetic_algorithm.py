import random
from matplotlib import pyplot as plt

from generate_dataset import generate_dataset
from overlap_methods import overlap_score_pigeonhole
from evaluation_methods import shingles_score
import genetic_algorithm_utilities


def GeneticAlgorithm(size=100, generations=500, select_n=60):

    reads = ["ac", "bc", "ab", "baabba"]
    reads1 = ["x", "y", "ax", "yb"]


    gau = genetic_algorithm_utilities.GeneticAlgorithmUtil(reads, reads1)

    population = gau.initialize_population(size)
    print("population is initialised...")
    print(population)

    max_so_far = {'genome': '', 'genome1':'', 'score': -10000}

    count = 1
    while count <= generations:

        for i in population:

            score = gau.fitness_score(population[i])

            index_list = population[i]
            print(index_list)
            genome1 = ''.join([reads1[j] for j in index_list])

            print("genome1", genome1, population[i])


            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['genome1'], max_so_far['score'] = i, genome1, score
                print("Max Score so far :", max_so_far['score'])
            if i == genome1:
                print("Success : ", i, population[i], genome1)
                exit()

        population, fitness = gau.selection(population, select_n, gau.fitness_score)

        print("Selection done")

        while len(population) < size:
            # print(len(population), size)
            temp = list(population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                # print("CHeck", a, b)

                # start = random.randint(1, len(a) - 2)
                # end = random.randint(start + 1, len(a))
                # genome_new, index_list = gau.crossover1(a, b, start, end)
                point_of_crossover = random.randint(0, len(a))
                index_list = a[:point_of_crossover] + b[point_of_crossover:]
                genome_new = gau.generate_genome(index_list, 0)
                # genome_new, index_list = gau.crossover_edge_recombination(a, b)
                if genome_new not in population:
                    population[genome_new] = index_list

        print("Crossover done")

        # mutation
        for i in list(population.keys()):
            temp = gau.mutation(population[i])
            temp_gen = gau.generate_genome(temp, 0)
            if temp_gen not in population:
                population.pop(i)
                population[temp_gen] = temp

        print("Generation :", count,max_so_far['score'])

        count += 1

        # print("Population len", len(population))

    return max_so_far['genome'], max_so_far['score']


if __name__ == '__main__':
    reconstructed_genome, score = GeneticAlgorithm()

    print("Best Score :", score)
