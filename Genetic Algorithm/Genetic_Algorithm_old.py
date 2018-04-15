import sys
import random

sys.path.append('../Dataset')
from Generate_Dataset import *

sys.path.append('../Evaluation Methods')
from Shingles_Score import *

sys.path.append('../Approximate APSP Methods')
from Overlap_Score_Pigeonhole import *

from Genetic_Algorithm_Utilities import *


def GeneticAlgorithm(size = 500, generations = 100, select_n = 60, threshold = 0.99, start = 5, end = 15):
    
    gd = GenerateDataset(error_rate = 0.6, mutation_rate = 0.6)
    genome = gd.random_genome(length = 1000)
    reads = gd.random_reads(length = 60, num = 500)
    
    osp = OverlapScorePigeonhole(reads)
    overlap_matrix = osp.overlap_scores()
    
    ss = ShinglesScore(n = 22)
    
    gau = GeneticAlgorithmUtilities(reads, overlap_matrix)
    
    population = gau.initialize_population(size)
    
    count = 1
    while count <= generations:
        

        population, fitness = gau.selection(population, select_n, gau.fitness_score1)
        
        max_so_far = {'genome':'', 'score':-10}
        for i in population:
            score = ss.ng_score(i, genome)
            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['score'] = i, score
            if  score >= threshold:                
                print("Genome Found! in generation", count, score)
                return i, score
        
        while len(population) < size:
            #print(len(population), size)
            temp = list(population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                #print("CHeck", a, b)
                genome, index_list = gau.crossover1(a, b, start, end)
                if genome not in population:
                    population[genome] = index_list
        
        #mutation
        for i in list(population.keys()):
            temp = gau.mutation(population[i])
            population.pop(i)
            temp_gen = gau.generate_genome(temp)
            population[temp_gen] = temp
    
        print("Generation :", count, max_so_far['score'])
        count += 1

    return max_so_far['genome'], max_so_far['score']   
    
    
    
    
if __name__ == '__main__':
    reconstructed_genome, score = GeneticAlgorithm()
    
    print("Best Score :", score)
    

