# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:41:09 2020

@author: arutk
"""

import general as g
import numpy as np

def _vikor(decision_matrix, weights, criteria_types=None):
    v = 0.5
    
    no_alternatives, no_criterias = decision_matrix.shape
    
    if criteria_types is None:
        criteria_types = ['P'] * no_criterias
        
    best, worst = calculateBestWorst(decision_matrix, no_criterias, criteria_types)
    auxiliary_matrix = calculateAuxiliaryDecisionMatrix(decision_matrix, no_alternatives, no_criterias, weights, best, worst)
    S_i, R_i = calculateSiRi(auxiliary_matrix, no_alternatives)
    Qi = calculateQi(S_i, R_i, v, no_alternatives)
    ranking = g.calculateRanking(Qi, desc="False")   
    return ranking

def calculateBestWorst(decision_matrix, no_criterias, criteria_types):
    best = []
    worst = []
    for i in range(no_criterias):
        if criteria_types[i] == "P":
            best.append(decision_matrix[:,i].max())
            worst.append(decision_matrix[:,i].min())
        else: 
            best.append(decision_matrix[:,i].min())
            worst.append(decision_matrix[:,i].max())
    return best, worst

def calculateAuxiliaryDecisionMatrix(decision_matrix, no_alternatives, no_criterias, weights, best, worst):
    auxiliary_matrix = np.zeros(shape=(no_alternatives, no_criterias))
    for i in range(no_criterias):
        for j in range(no_alternatives):
            auxiliary_matrix[j][i] = weights[i] * (best[i] - decision_matrix[j][i])/(best[i] - worst[i])
    return auxiliary_matrix

def calculateSiRi(auxiliary_matrix, no_alternatives):
    S_i = []
    R_i = []
    for i in range(no_alternatives):
        S_i.append(auxiliary_matrix[i,:].sum())
        R_i.append(auxiliary_matrix[i,:].max())
    return S_i, R_i

def calculateQi(S_i, R_i, v, no_alternatives):
    S_star, R_star, S_minus, R_minus = getSsAndRs(S_i, R_i)
    Q_i = []
    for i in range(no_alternatives):
        Q_i.append(v * (S_i[i] - S_star)/(S_minus - S_star) + v * (R_i[i] - R_star)/(R_minus - R_star))
    return Q_i

def getSsAndRs(S_i, R_i):
    return min(S_i), min(R_i), max(S_i), max(R_i)
