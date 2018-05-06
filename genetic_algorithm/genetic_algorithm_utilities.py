import random
import time


class GeneticAlgorithmUtil:

    def __init__(self, reads, reads1):
        self.reads = reads
        self.reads1 = reads1
        self.reads_n = len(reads)

    def generate_genome(self, index_list, choice):
        first = (choice == 0)
        genome = ''.join([self.reads[j] if first else self.reads1[j] for j in index_list])

        return genome

    def initialize_population(self, size, length = 10):
        random.seed(time.time())
        i = 0
        population = dict()
        while i < size:
            genome = ''
            index_list = []
            genome_len = random.randint(1, length)
            while len(genome) < genome_len:
                index = random.choice(list(range(self.reads_n)))
                index_list.append(index)
                genome += self.reads[index]

            if genome not in population:
                # print(genome)
                population[genome] = index_list
                i += 1

        return population

    def fitness_score(self, index_list):

        genome, genome1 = self.generate_genome(index_list, 0), self.generate_genome(index_list, 1)
        length, length1 = len(genome), len(genome1)

        score = 0 - abs(length - length1)
        score += sum([1 if genome[i] == genome1[i] else 0 for i in range(min(length, length1))])

        return score

    def selection(self, population, n, fn):
        new_population = {}
        fitness = {}
        for i in population:
            fitness[i] = fn(population[i])
        ordered = sorted(fitness.items(), key=lambda x: x[1], reverse=True)
        # print("ordered", len(ordered))
        for i in range(n):
            genome = ordered[i][0]
            new_population[genome] = population[genome]
        return new_population, fitness

    def mutation(self, index_list):
        t = len(index_list)
        random.seed(time.time())

        a = random.randint(0, t - 1)
        b = random.randint(0, t - 1)

        index_list[a], index_list[b] = index_list[b], index_list[a]

        return index_list

    def crossover(self, a, b):
        point_of_crossover = random.randint(0, len(a) - 1)

        index_list = a[:point_of_crossover] + b[point_of_crossover:]
        genome_new = self.generate_genome(index_list, 0)

        return genome_new, index_list


if __name__ == '__main__':
    reads = ["ab", "ba", "aaa", "bbb"]
    reads1 = ["abb", "aaa", "ab", "bb"]

    u = GeneticAlgorithmUtil(reads, reads1)

    print(u.generate_genome([3,3], 0))
    print(u.generate_genome([3,3], 1))
    print(u.initialize_population(2))
    print(u.fitness_score([1,0,1,1,1]))
    print("crossover", u.crossover([1,0,1,1,0,0], [1,0,1,1,1,1]))
    print("mutation", u.mutation([1,0,1,1,1,1]))
    print("done")
