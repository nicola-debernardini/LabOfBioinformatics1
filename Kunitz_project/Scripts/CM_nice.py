#!/urs/bin/python

######### CONFUSION MATRIX ##########
# This program takes in input a file cotaining the entries classified in two classes (0 and 1) and a threshold 
# and it is able to calculate the confusion matrix and other parameters like the accuracy, the Matthew's correlation coefficient,
# the sensitivity and the false positive rate. 
#########

import sys
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the confusion matrix:
def conf_mat(filename, th, sp, cp =-1):     # cp: class position  
    cm = [[0,0],[0,0]]      # Initialize the confusion matrix
    f = open(filename) 

    # Fill in the Confusion matrix:
    for line in f:
        v = line.rstrip().split()

        if int(v[cp]) == 1: # It belong to the positive set -> kunitz
            j = 1 
        else: # It belong to the negative set -> non-kunitz
            j = 0 
        if float(v[sp]) < th:  # Predicted as kunitz
            i = 1
        else: # Predicted as non-kunitz 
            i = 0 

        cm[i][j] = cm[i][j] +1

        # Confusion matrix topology:
        #        REAL    N-K         K
        #   PRED N-K   0,0 TN     0,1 FN
        #         K    1,0 FP     1,1 TP            

    return cm

# Function to calculate the model performance:
def print_performance(cm):
    acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][1]+cm[1][0]+cm[0][1]) # Accuracy (Q2)
    d = np.sqrt((cm[0][0]+cm[0][1])*(cm[0][0]+cm[1][0])*(cm[1][1]+cm[0][1])*(cm[1][1]+cm[1][0])) # MCC denominator 
    mc = (cm[0][0]*cm[1][1]-cm[0][1]*cm[1][0])/d # Matthew's correlation coefficient  
    n = float(sum(cm[0])+sum(cm[1]))
    
    print '\nThe confusion matrix is:\n', cm
    print '\nParameter:\n','Q2 = ', acc,'MCC = ', mc, 'FPR = ', float(cm[1][0])/(float(cm[1][0])+float(cm[0][0])), 'TPR =',  float(cm[1][1])/(float(cm[1][1])+float(cm[0][1])) 

# This function prints and plots the confusion matrix. 
def plot_confusion_matrix(cm, normalize=False, title=None, cmap=plt.cm.YlGn): # Normalization can be applied by setting `normalize=True`.
    cm = np.array(cm)
    
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix'

    classes = ['Non-Kunitz', 'Kunitz']

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix") 
    else:
        print('Confusion matrix')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Predicted label',
           xlabel='True label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


# MAIN #
if __name__=='__main__':
    filename = sys.argv[1] # file in input containing the entry, the E-value and the class
    th = float(sys.argv[2]) # E-value treashold 
    sp = -2 # score position: E-value column  

    # Option to calcultate the mean of two threshold took in input
    if len(sys.argv) > 3: # If the user pass to the program an extra threshold the th value will become the average of the two threshold 
        th1 = float(sys.argv[3])
        th = (th+th1)/2
         
    cm = conf_mat(filename,th,sp)
    print_performance(cm)
    print '\nThe threashold used is = ', th 
    np.set_printoptions(precision=2)
    
    # Plot non-normalized confusion matrix
    plot_confusion_matrix(cm, title='Confusion matrix')
    plt.savefig('CM.png')
    
    # Plot normalized confusion matrix
    plot_confusion_matrix(cm, normalize=True, title='Normalized confusion matrix')
    plt.savefig('Norm_CM.png')
    plt.show()







