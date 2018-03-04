# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:03:03 2018

@author: KRUTHI
"""
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import random

scale = 3
extreme = 10
size = 10000
genes = ['A', 'G', 'T', 'C']

def int_to_gene(n):
    if -10 <= n < -2.5:
        return 'A'
    elif -2.5 <= n < 0:
        return 'G'
    elif 0 <= n < 2.5:
        return 'T'
    else:
        return 'C'
    
def induce_error(read, error_rate, mutation_rate):
    
    for i in range(int(len(read) * mutation_rate)):
        random_index = random.randint(0, len(read) - 1)
        
        rn = random.random()
        
        if rn < error_rate:
            read = read[:random_index] + random.choice([c for c in genes if genes != read[random_index]]) + read[random_index+1:]
        
         
    return read

def random_genome(length = 1000):
    
    numbers = truncnorm(a = -extreme/scale, b = extreme/scale, scale = scale).rvs(size = size) 
    numbers = numbers.round().astype(int)
    

    plt.hist(numbers, 2 * extreme + 1)
    
    genome = ''.join([int_to_gene(n) for n in numbers])
    
    return genome

def random_reads(genome, length = 20, num = 5):
    reads = []
    for i in range(num):
        start = random.randint(0, len(genome) - length)
        
        read = genome[start:start + length]
        
        read = induce_error(read, 0.8, 0.6)
        
        reads.append(read)
        
    return reads

genome = random_genome()
print(genome)
reads = random_reads(genome)
count = 1
for read in reads:
    print("Read", count, read)
    count += 1