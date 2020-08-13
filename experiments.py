# -*- coding: utf-8 -*-
"""
Created on Thu May 28 20:56:53 2020

@author: arutk
"""

import general as g
from topsis import _topsis
from vikor import _vikor
from promethee import _prometheeII
import copy
import numpy as np

def exp_topsis(norm_matrixes, weights_list):
    matrixes_intervals = []
    # matrixes_rankings = []

    for num, matrix in enumerate(norm_matrixes):
        r0 = _topsis(matrix, weights_list[num])
        no_alternatives, no_criterias = matrix.shape
        intervals = np.zeros(shape=(no_criterias, 2))
        # rankings = np.zeros(shape=(no_criterias, no_alternatives))
        
        for i in range(no_criterias):
            copy_min = copy.deepcopy(weights_list[num])
            while True:
                if copy_min[i] == 0.0001:
                    break
                
                copy_min = g.adjustWeights(copy_min, no_criterias, i, type=True)
                r = _topsis(matrix, copy_min)
                
                if g.calculateRS(r0, r) != 1:
                    break
                
            max_weights = copy.copy(weights_list[num])
            while True:
                copy_max = g.adjustWeights(max_weights, no_criterias, i, type=False)
                if copy_max[i] == 0.9999:
                    break
    
                r = _topsis(matrix, copy_max)
                
                if g.calculateRS(r0, r) != 1:
                    break  
                
            intervals[i,:] = [copy_min[i], copy_max[i]]
        matrixes_intervals.append(intervals)
    
    print(g.latex_export(matrixes_intervals))
    return matrixes_intervals
    
def exp_vikor(matrixes, weights_list):
    matrixes_intervals = []

    for num, matrix in enumerate(matrixes):
        r0 = _vikor(matrix, weights_list[num])
        no_criterias = matrix.shape[1]
        intervals = np.zeros(shape=(no_criterias, 2))
        
        for i in range(no_criterias):
            copy_min = copy.deepcopy(weights_list[num])
            while True:
                if copy_min[i] == 0.0001:
                    break
                
                copy_min = g.adjustWeights(copy_min, no_criterias, i, type=True)
                r = _vikor(matrix, copy_min)
                
                if g.calculateRS(r0, r) != 1:
                    break
                
            max_weights = copy.copy(weights_list[num])
            while True:
                copy_max = g.adjustWeights(max_weights, no_criterias, i, type=False)
                if copy_max[i] == 0.9999:
                    break
    
                r = _vikor(matrix, copy_max)
                
                if g.calculateRS(r0, r) != 1:
                    break  
                
            intervals[i,:] = [copy_min[i], copy_max[i]]
        matrixes_intervals.append(intervals)
    
    print(g.latex_export(matrixes_intervals))
    return matrixes_intervals
    
def exp_promethee(matrixes, weights_list):
    matrixes_intervals = []

    for num, matrix in enumerate(matrixes):
        r0 = _prometheeII(matrix, weights_list[num])
        no_criterias = matrix.shape[1]
        intervals = np.zeros(shape=(no_criterias, 2))
        
        for i in range(no_criterias):
            copy_min = copy.deepcopy(weights_list[num])
            while True:
                if copy_min[i] == 0.0001:
                    break
                
                copy_min = g.adjustWeights(copy_min, no_criterias, i, type=True)
                r = _prometheeII(matrix, copy_min)
                
                if g.calculateRS(r0, r) != 1:
                    break
                
            max_weights = copy.copy(weights_list[num])
            while True:
                copy_max = g.adjustWeights(max_weights, no_criterias, i, type=False)
                if copy_max[i] == 0.9999:
                    break
    
                r = _prometheeII(matrix, copy_max)
                
                if g.calculateRS(r0, r) != 1:
                    break  
                
            intervals[i,:] = [copy_min[i], copy_max[i]]
        matrixes_intervals.append(intervals)
    
    print(g.latex_export(matrixes_intervals))
    return matrixes_intervals
    
def main():
    no = [3, 5, 10]
    matrixes = g.generateMatrixes(no)
    g.latex_export(matrixes)

    norm_matrixes = g.normalizeMatrixes(matrixes, normalization_method='MinMax')
    g.latex_export(norm_matrixes)
    
    criterias_list = [3, 5, 10, 3, 5, 10, 3, 5, 10]
    weights_list = g.generateWeights(criterias_list)
    print(f'wagi: {weights_list}')
    
    intervals_topsis = exp_topsis(matrixes, weights_list)
    g.plotIntervals(intervals_topsis, 'Topsis')
    
    intervals_vikor = exp_vikor(norm_matrixes, weights_list)
    g.plotIntervals(intervals_vikor, 'VikorMinMax')

if if __name__ == "__main__":
    main()
        