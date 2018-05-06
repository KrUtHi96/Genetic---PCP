import random
import genetic_algorithm_utilities


def GeneticAlgorithm(size=100, generations=500, select_n=60):

    reads = ["abc", "d", "ef"]
    reads1 = ["ab", "cde", "fg"]

    gau = genetic_algorithm_utilities.GeneticAlgorithmUtil(reads, reads1)

    population = gau.initialize_population(size)

    # print("population is initialised...")
    # print(population)

    max_so_far = {'genome': '', 'genome1': '', 'score': -10000}

    count = 1
    while count <= generations:

        for i in population:

            score = gau.fitness_score(population[i])

            index_list = population[i]
            genome1 = gau.generate_genome(index_list, 1)

            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['genome1'], max_so_far['score'] = i, genome1, score
                print("Max Score so far :", max_so_far['score'])

            if i == genome1:
                print("Success : ", i, population[i])
                exit()

        population, fitness = gau.selection(population, select_n, gau.fitness_score)
        # print("Selection done")

        # population regeneration
        while len(population) < size:
            temp = list(population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                genome_new, index_list = gau.crossover(a, b)

                if genome_new not in population:
                    population[genome_new] = index_list
        # print("Crossover done")

        # mutation
        for i in list(population.keys()):
            temp = gau.mutation(population[i])
            temp_gen = gau.generate_genome(temp, 0)
            if temp_gen not in population:
                population.pop(i)
                population[temp_gen] = temp

        print("##### Generation : {} has max score {} ########".format(count, max_so_far['score']))
        count += 1

    return max_so_far['genome'], max_so_far['score']


if __name__ == '__main__':
    reconstructed_genome, score = GeneticAlgorithm()

    print("Best Score :", score)
