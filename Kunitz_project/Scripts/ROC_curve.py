#!/urs/bin/


############ SCRIPT ##############
# Given in input a file containing the entries, the score and the class to which they belong this script is able to calculate the ROC curve  

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

# Finction to calculate and represent the ROC curve 
def ROC(filename, sp):    
    score = []
    y = []

    file = open(filename)
    for line in file:
        l = line.rstrip().split()
        score.append(-float(l[sp]))
        y.append(int(l[-1]))

    score = np.array(score)
    y = np.array(y)

    # CALCULATE THE ROC DATA 
    fpr, tpr, thresholds = metrics.roc_curve(y, score, pos_label=1)
    roc_auc = metrics.auc(fpr, tpr)

    # PRINT THE PLOT OF THE ROC CURVE
    plt.figure()    
    lw = 2 # linewidth 
    plt.plot(fpr, tpr, color='darkorange', lw =lw, label='ROC curve (area = %0.4f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.savefig('ROC.png')
    plt.show()
    plt.savefig("ROC_curve.png")


if __name__=='__main__':
    filename = sys.argv[1] # file containing the ID and a column with the E-value and the class 
    sp = -2 # score position is the second last column
    if len(sys.argv) > 2: sp = int(sys.argv[2])-1 # From command line is possible to change the default column of the E-value
    ROC(filename,sp)
    
    

