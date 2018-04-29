import random

from generate_dataset import generate_dataset
from overlap_methods import overlap_score_pigeonhole
from evaluation_methods import shingles_score
import genetic_algorithm_utilities


def GeneticAlgorithm(size=100, generations=60, select_n=60, threshold=0.99):
    gd = generate_dataset.GenerateDataset(error_rate=0, mutation_rate=0)
    genome = gd.random_genome(length=3000)

    reads = gd.random_reads(length=600, num=4000)
    print("Getting overlap matrix")
    osp = overlap_score_pigeonhole.OverlapScorePigeonhole(reads, overlap_minimum=20, max_error=3)
    overlap_matrix = osp.overlap_scores()

    print("************matrix computed********************")

    ss = shingles_score.ShinglesScore(n=12)

    gau = genetic_algorithm_utilities.GeneticAlgorithmUtil(reads, overlap_matrix)

    population = gau.initialize_pop(size, len(genome)) #Works..
    #population = gau.initialize_population(size)

    max_so_far = {'genome': '', 'score': -10}

    count = 1
    while count <= generations:

        for i in population:
            # print("population",len(i),"original", len(genome))
            score = ss.ng_score(i, genome)

            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['score'] = i, score
                print("Max Score so far :", max_so_far['score'])
            if score >= threshold:
                print("Genome Found! in generation", count, score)
                return i, score

        population, fitness = gau.selection(population, select_n, gau.fitness_score2)

        print("Selection done")

        while len(population) < size:
            # print(len(population), size)
            temp = list(population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                # print("CHeck", a, b)

                start = random.randint(1, len(a) - 2)
                end = random.randint(start + 1, len(a))
                genome_new, index_list = gau.crossover1(a, b, start, end)

                # genome_new, index_list = gau.crossover_edge_recombination(a, b)
                if genome_new not in population:
                    population[genome_new] = index_list

        print("Crossover done")

        # mutation
        for i in list(population.keys()):
            temp = gau.mutation_pop(population[i])
            temp_gen = gau.generate_genome(temp)
            if temp_gen not in population:
                population.pop(i)
                population[temp_gen] = temp

        print("Generation :", count, max_so_far['score'])
        count += 1

        print("Population len", len(population))

    return max_so_far['genome'], max_so_far['score']


if __name__ == '__main__':
    reconstructed_genome, score = GeneticAlgorithm()

    print("Best Score :", score)
