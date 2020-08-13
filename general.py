# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:26:59 2020

@author: arutk
"""

import math
import numpy as np
import scipy.stats as ss
import random
from tabulate import tabulate
import matplotlib.pyplot as plt

# NORMALIZACJE
def normalizeMatrixes(matrixes, normalization_method='Max'):  
    normalized_matrixes = []
    
    if normalization_method == 'Max':
        for matrix in matrixes:
            normalized_matrixes.append(normalizeMatrixMax(matrix))          
    elif normalization_method == 'MinMax':
        for matrix in matrixes:
            normalized_matrixes.append(normalizeMatrixMinMax(matrix))
    else:
        for matrix in matrixes:
            normalized_matrixes.append(normalizedMatrix = normalizeMatrixRoot(matrix))
    return normalized_matrixes

def normalizeMatrixMax(decision_matrix, criteria_types=None):
    no_alternatives, no_criterias = decision_matrix.shape
    
    if criteria_types is None:
        criteria_types = ['P'] * no_criterias
        
    normalized_matrix = np.zeros(shape=(no_alternatives, no_criterias))
    for i in range(no_criterias):
        maximum = decision_matrix[:,i].max()
        for j in range(no_alternatives):
            if criteria_types[i] == 'P':
                normalized_matrix[j][i] = decision_matrix[j][i]/maximum
            elif criteria_types[i] == 'C':
                normalized_matrix[j][i] = 1 - (decision_matrix[j][i]/maximum)
    return normalized_matrix            

def normalizeMatrixMinMax(decision_matrix, criteria_types=None):
    no_alternatives, no_criterias = decision_matrix.shape
    
    if criteria_types is None:
        criteria_types = ['P'] * no_criterias
    
    normalized_matrix = np.zeros(shape=(no_alternatives, no_criterias))
    for i in range(no_criterias):
        maximum = decision_matrix[:,i].max()
        minimum = decision_matrix[:,i].min()
        for j in range(no_alternatives):
            if criteria_types[i] == 'P':
                normalized_matrix[j][i] = (decision_matrix[j][i] - minimum)/(maximum - minimum)
            elif criteria_types[i] == 'C':
                normalized_matrix[j][i] = (maximum - decision_matrix[j][i])/(maximum - minimum)
    return normalized_matrix

def normalizeMatrixRoot(decision_matrix, criteria_types=None):
    no_alternatives, no_criterias = decision_matrix.shape
    
    if criteria_types is None:
        criteria_types = ['P'] * no_criterias
    
    normalized_matrix = np.zeros(shape=(no_alternatives, no_criterias))
    for i in range(no_criterias):
        root_sum_of_powers = math.sqrt(sum(np.power(decision_matrix[:,i], 2)))
        for j in range(no_alternatives):
            if criteria_types[i] == 'P':
                normalized_matrix[j][i] = decision_matrix[j][i]/root_sum_of_powers
            elif criteria_types[i] == 'C':
                normalized_matrix[j][i] = 1 - (decision_matrix[j][i]/root_sum_of_powers)
    return normalized_matrix 

# INNE
def generateMatrixes(no):    
    matrixes = []
    for i in no:
        for j in no:
            matrixes.append(makeRandomDecisionMatrix(i, j))
    return matrixes

def makeRandomDecisionMatrix(no_alternatives, no_criterias, mean=10, sigma=3):
    np.random.seed(42)
    return np.random.normal(mean, sigma, size=(no_alternatives, no_criterias))

def calculateRanking(vector, desc=True):
    if desc:
        return len(vector) - ss.rankdata(vector) + 1
    else:
        return ss.rankdata(vector)

def calculateRS(ran1, ran2):
    if len(ran1) != len(ran2):
        print('Lengths of vectors does not match.')
    else:
        summ = np.sum(np.power((np.array(ran1) - np.array(ran2)),2))
        return 1 - ((6 * summ)/(len(ran1) * (len(ran1)**2 - 1)))
    
# EKSPERYMENTY
# tworzenie macierzy decyzyjnych
def generateWeights(criterias_list):
    mat_weights = []
    for no in criterias_list:    
        mat_weights.append(randomWeights(no))
    return mat_weights

def randomWeights(no_criterias):
    random.seed(42)
    list_ = []
    for i in range(no_criterias):
        list_.append(random.uniform(0, 1))
    weights = np.array(list_)
    weights /= weights.sum()
    return weights

def adjustWeights(weights, n, index, type=True, value=0.0001):
    v = value/(n - 1)
    if type: 
        for i in range(n):
            if i == index:
                weights[i] -= value
                if weights[i] <= 0:
                    weights[i] = 0.0001
            else:              
                weights[i] += v

    else:
        for i in range(n):
            if i == index:
                weights[i] += value
                if weights[i] >= 1:
                    weights[i] = 0.9999
            else:
                weights[i] -= v

    return weights

def latex_export(list_matrixes, decimal="0.4f"):
    for mat in list_matrixes:
        print('\n\n')
        print(tabulate(mat, tablefmt="latex", floatfmt=decimal))
        
def single_latex_export(data, decimal="0.4f"):
    print('\n')
    print(tabulate(data, tablefmt="latex", floatfmt=decimal))
        
def plotIntervals(matrixes_intervals, method):
    for i, intervals in enumerate(matrixes_intervals): 
        x = range(intervals.shape[0])
        y_min = intervals[:,0]
        y_max = intervals[:,1]
        plt.plot(x,y_min, 'bo')
        plt.plot(x,y_max, 'ro')
        plt.title(f'Wykres interwałów macierzy nr {i+1} \nw metodzie {method}')
        plt.savefig(f'./plots/{method}WykresInterwaluNr{i}.png')
        plt.show()
            
