"""
Created on Mon May 25 16:17:58 2020

@author: arutk
"""

import numpy as np
import math
import general as g

def _topsis(normalizedMatrix, weights):
    no_alternatives, no_criterias = normalizedMatrix.shape     
    weightedMatrix = calculateWeightedDecisionMatrix(normalizedMatrix, weights, no_alternatives, no_criterias)
    PIS, NIS = calculatePISNIS(weightedMatrix, no_criterias)
    dPlus, dMinus = calculateDPlusDMinus(weightedMatrix, PIS, NIS, no_alternatives, no_criterias)
    C = calculateC(dPlus, dMinus, no_alternatives)
    
    ranking = g.calculateRanking(C)
    # print(f'Ustalony ranking: {ranking}.')
    return ranking
            
def calculateWeightedDecisionMatrix(normalizedMatrix, weights, no_alternatives, no_criterias):
    weightedMatrix = np.zeros(shape=(no_alternatives, no_criterias))
    for i in range(no_alternatives):
        for j in range(no_criterias):
            weightedMatrix[i][j] = normalizedMatrix[i][j] * weights[j]
    return weightedMatrix

def calculatePISNIS(weightedMatrix, no_criterias):
    PIS = []
    NIS = []
    for i in range(no_criterias):
        PIS.append(weightedMatrix[:,i].max())
        NIS.append(weightedMatrix[:,i].min())
    return PIS, NIS
        
def calculateDPlusDMinus(weightedMatrix, PIS, NIS, no_alternatives, no_criterias):
    dPlus = []
    dMinus = []
    for i in range(no_alternatives):
        dPlus_value = 0
        dMinus_value = 0
        for j in range(no_criterias):
            dPlus_value += math.pow(weightedMatrix[i][j] - PIS[j], 2)
            dMinus_value += math.pow(weightedMatrix[i][j] - NIS[j], 2)  
        dPlus.append(math.sqrt(dPlus_value))
        dMinus.append(math.sqrt(dMinus_value)) 
    return dPlus, dMinus

def calculateC(dPlus, dMinus, no_alternatives):
    C = []
    for i in range(no_alternatives):
        C.append(dMinus[i]/(dMinus[i]+dPlus[i]))
    return C




