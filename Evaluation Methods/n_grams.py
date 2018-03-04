# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 12:45:29 2018

@author: KRUTHI
"""
import numpy as np
import matplotlib.pyplot as plt


def n_gram_i(text, start, n):
    return text[start:start + n]
    
def n_gram_set(text, n):
    
    S = set()
    
    N = len(text)
    
    for i in range(N - n + 1):
        S.add(n_gram_i(text, i, n))
        
    #print(S)
    
    return S
    
def ng_score(a, b, n = 3):
    
    dot_plot_matrix(a, b, n)
    
    S_a = n_gram_set(a, n)
    S_b = n_gram_set(b, n)
    
    score = len(S_a.intersection(S_b))
    
    score /= max(len(S_a), len(S_b))
    
    return score

def dot_plot_matrix(a, b, n):
    
    range_a = len(a) - n + 1
    range_b = len(b) - n + 1
    r, c = [], []
    matrix = np.zeros(shape = (range_a, range_b))
    
    for i in range(range_a):
        for j in range(range_b):
            
            if n_gram_i(a, i, n) == n_gram_i(b, j, n):
                if i == j:
                    matrix[i, j] = 0.5
                else:
                    matrix[i, j] = 1
            
    plt.imshow(matrix)

    #print(matrix)
    
    

def test(n = 3):
    
    a = "AACCCTAACCCTAACCCTAACCCTAACCCTAACCCCTAACCCTAACCCTACCCCTAACCCCCAACCCTCACACCAACCCTAACCCTACCCCCAACCCCAC"
    b = "AACCCTAACCCTAACCCTAACCCTAACCCTAACCCCTAACCCTAACCCTACCCCTAACCCCCAACCCTCACACCAACCCTAACCCTACCCCCAACCCCAC"
    
    score = ng_score(a, b, n)
    
    print("Global Similarity Score", score)
    
if __name__ == '__main__':
    test(12)
    
    