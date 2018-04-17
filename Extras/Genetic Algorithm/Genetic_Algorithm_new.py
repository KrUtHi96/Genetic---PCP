import sys
import random

sys.path.append('../Dataset')
from Generate_Dataset import *

sys.path.append('../Evaluation Methods')
from Shingles_Score import *

sys.path.append('../Approximate APSP Methods')
from Overlap_Score_Pigeonhole import *

from Genetic_Algorithm_Utilities import *


class GeneticAlgorithm:

    
    def __init__(self, size = 500, generations = 100, select_n = 60, threshold = 0.99, start = 5, end = 15):
        
        self.size = size
        self.generations = generations
        self.select_n = select_n
        self.threshold = threshold
        self.start = start
        self.end = end

        self.gd = GenerateDataset(error_rate = 0.6, mutation_rate = 0.5)
        self.genome = self.gd.random_genome(length = 1000)
        self.reads = self.gd.random_reads(length = 60, num = 500)

        self.osp = OverlapScorePigeonhole(self.reads)
        self.overlap_matrix = self.osp.overlap_scores()

        self.ss = ShinglesScore(n = 22)

        self.gau = GeneticAlgorithmUtilities(self.reads, self.overlap_matrix)

        self.population = self.gau.initialize_population(self.size)


    def find_max_so_far(self):

        max_so_far = {'genome':'', 'score':-10}
        for i in self.population:
            print(len(i), len(self.genome))
            score = self.ss.ng_score(i, self.genome)
            print(score)
            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['score'] = i, score
        return max_so_far


    def perform_crossover(self):
        while len(self.population) < self.size:
            # print(len(self.population), self.size)
            temp = list(self.population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                # print("Check", a, b)
                new_genome, index_list = self.gau.crossover1(a, b, self.start, self.end)
                if new_genome not in self.population:
                    self.population[new_genome] = index_list


    def perform_mutation(self):
        for i in list(self.population.keys()):
            temp = self.gau.mutation(self.population[i])
            self.population.pop(i)
            temp_gen = self.gau.generate_genome(temp)
            
            self.population[temp_gen] = temp


    def run(self):

        count = 1
        while count <= self.generations:

            # Selection
            self.population, fitness = self.gau.selection(self.population, self.select_n, self.gau.fitness_score1)

            # Finding max so far and returning if threshold reached
            max_so_far = self.find_max_so_far()
            if  max_so_far['score'] >= self.threshold:                
                print("Genome Found! in generation", count, max_so_far['score'])
                return max_so_far['genome'], max_so_far['score']

            # Crossover
            self.perform_crossover()

            #mutation
            self.perform_mutation()

            print("Generation :", count, max_so_far['score'])
            count += 1

        return max_so_far['genome'], max_so_far['score']   


if __name__ == '__main__':

    ga = GeneticAlgorithm()
    reconstructed_genome, score = ga.run()

    print("Best Score :", score)