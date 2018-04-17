import sys
import random

sys.path.append('../Dataset')
from Generate_Dataset import *

sys.path.append('../Evaluation Methods')
from Shingles_Score import *

sys.path.append('../Approximate APSP Methods')
from Overlap_Score_Pigeonhole import *

from Genetic_Algorithm_Utilities import *


def GeneticAlgorithm(size = 1000, generations = 100, select_n = 60, threshold = 0.99, start = 2, end = 7):
    
    gd = GenerateDataset(error_rate = 0, mutation_rate = 0)
    genome = gd.random_genome(length = 21)
 
    reads = gd.random_reads(length = 3, num = 7)
    
    osp = OverlapScorePigeonhole(reads, overlap_minimum = 4, max_error = 0)
    
    overlap_matrix = osp.overlap_scores()
    '''
    for row in range(len(reads)):
        for col in range(len(reads)):
            if overlap_matrix[row, col]:
                print(overlap_matrix[row, col])
    '''
                
    ss = ShinglesScore(n = 6)
    
    gau = GeneticAlgorithmUtilities(reads, overlap_matrix)
    
    population = gau.initialize_population(size)
    
    max_so_far = {'genome':'', 'score':-10}
    
    count = 1
    while count <= generations:
        
        
        
        
        population, fitness = gau.selection(population, select_n, gau.fitness_score2)
        
        print("Population len", len(population))
        
        
    
        while len(population) < size:
            #print(len(population), size)
            temp = list(population.values())
            a = random.choice(temp)
            b = random.choice(temp)
            if a != b:
                #print("CHeck", a, b)
                genome_new, index_list = gau.crossover1(a, b, start, end)
                if genome_new not in population:
                    population[genome_new] = index_list
                    
        print("pop", len(population))
        
        #mutation
        for i in list(population.keys()):           
            temp = gau.mutation(population[i])
            temp_gen = gau.generate_genome(temp)
            if temp_gen not in population:
                population.pop(i)            
                population[temp_gen] = temp
                
        for i in population:
            #print("population",len(i),"original", len(genome))
            score = ss.ng_score(i, genome)
    
            if score > max_so_far['score']:
                max_so_far['genome'], max_so_far['score'] = i, score
                print(max_so_far['score'])
            if  score >= threshold:                
                print("Genome Found! in generation", count, score)
                return i, score
    
        print("Generation :", count, max_so_far['score'])
        count += 1
        
        print("Population len", len(population))

    return max_so_far['genome'], max_so_far['score']   
    
    
    
    
if __name__ == '__main__':
    reconstructed_genome, score = GeneticAlgorithm()
    
    print("Best Score :", score)
    

