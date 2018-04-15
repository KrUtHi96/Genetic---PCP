import random


class GeneticAlgorithmUtilities:

    
    def __init__(self, reads, overlap_matrix):
        
        self.reads = reads
        self.overlap_matrix = overlap_matrix
        
        self.reads_n = len(reads)
        

    def add(self, i, j):
        
        offset = int( self.overlap_matrix[i][j] )
        return self.reads[j][offset:]


    def generate_genome(self, index_list):
        
        genome = self.reads[index_list[0]]
        for i in range(1, len(index_list)):
            genome += self.add(index_list[i - 1], index_list[i])
        return genome


    def initialize_population(self, size):

        i = 0
        population = {} 
        while i < size:
            index_list = [] 
            temp = list(range(self.reads_n))
            while temp:
                index = random.choice(temp)
                temp.remove(index)
                index_list.append(index)
            genome = self.generate_genome(index_list)
            if genome not in population:
                population[genome] = index_list
                i += 1
        return population


    def fitness_score1(self, index_list):

        score = 0
        for i in range(len(index_list) - 1):
            score += self.overlap_matrix[index_list[i]][index_list[i + 1]]
        return score


    def fitness_score2(self, index_list):

        score = 0
        for i in range(len(index_list) - 1):
            for j in range(len(index_list) - 1):
                score = score + (abs(i - j) * self.overlap_matrix[index_list[i]][index_list[j]])
        return score


    def selection(self, population, n, fn):

        new_population = {}
        fitness = {}
        for i in population:
            fitness[i] = fn(population[i])
        ordered = sorted(fitness.items(), key = lambda x : x[1], reverse = True)
        for i in range(n):
            genome = ordered[i][0]
            new_population[genome] = population[genome]
        return new_population, fitness


    def crossover1(self, p1, p2, start, end):

        temp = p1[start : end + 1]
        count = 0
        for i in p2:
            if i not in temp:
                if count < start:
                    temp = [i] + temp
                else:
                    temp = temp + [i]
                count += 1
        temp = self.mutation(temp)
        genome = self.generate_genome(temp)
        return genome, temp


    def mutation(self, index_list):
    	
        a = random.randint(0, self.reads_n - 1)
        b = random.randint(0, self.reads_n - 1)
        index_list[a], index_list[b] = index_list[b], index_list[a]
        return index_list


if __name__ == '__main__':
    pass