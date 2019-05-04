#!/urs/bin/python

############ SCRIPT ##############
# This script can determine which is the optimal threshold for the model in a specific dataset   

import sys
import numpy as np

# Function to calculate the confusion matrix
def conf_mat(filename, th, sp = -2, cp =-1): # Used to defive default variables in a function: score position, class position 
    cm = [[0.0,0.0],[0.0,0.0]] # Confusion matrix
    f = open(filename) 
    for line in f:
        v = line.rstrip().split()
        
        if int(v[cp]) == 1: 
            j = 1 # It belong to the positive set -> kunitz
        else:
            j = 0 # It belong to the negative set -> non-kunitz
        if float(v[sp]) < th: 
            i = 1 # Predicted as kunitz
        else:
            i = 0 # Predicted as non-kunitz 

        #        REAL    N-K         K
        #   PRED N-K   0,0 TN     0,1 FN
        #         K    1,0 FP     1,1 TP            

        cm[i][j] = cm[i][j] +1

    return cm

# Function to calculate the perfomance given a confusion matrix 
def print_performance(cm, th):

    acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][1]+cm[1][0]+cm[0][1])
    d = np.sqrt((cm[0][0]+cm[0][1])*(cm[0][0]+cm[1][0])*(cm[1][1]+cm[0][1])*(cm[1][1]+cm[1][0])) #denominator 
    if d == 0:
        d = 1

    mc = (cm[0][0]*cm[1][1]-cm[0][1]*cm[1][0])/d # Mathew correlation 
    n = float(sum(cm[0])+sum(cm[1]))
    FPR = float(cm[1][0])/(float(cm[1][0])+float(cm[0][0]))    # FPR = FP /(FP+TN)   
    TPR = float(cm[1][1])/(float(cm[1][1])+float(cm[0][1]))    # TPR = TP /(TP+FN)

    print cm, 'TH = ', th, 'Q2 = ', acc, 'MCC = ', mc, 'FPR = ', FPR, 'TPR =', TPR
    return mc

# MAIN #
if __name__=='__main__':
    filename = sys.argv[1]
    sp = -2 
    if len(sys.argv) > 2: sp = int(sys.argv[2])-1 # From command line is possible to change the default column of the E-value
    
    optimal = float('-inf')
    optimal_th = 0 

    som = 0
    recursion = 30 
    th = 1.0

    # Cycle through different threshold and evaluate the performance 
    for i in range(recursion):
        th = th/2.0   
        cm = conf_mat(filename, th, sp)
        som = print_performance(cm, th)

    # Save the threashold generating the higher MCC
        if som > optimal: 
            optimal = som 
            optimal_th = th 

    print '> The optimal treashold is: ', optimal_th
    