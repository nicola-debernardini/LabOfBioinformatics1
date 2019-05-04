#!/usr/local/bin/python3

############ SCRIPT ##############
# This script normalize the values of a list of E-values according to the number of sequences present in the dataset 

import sys

def normalizator(eva,tot,out):
    f = open(eva)
    o = open(out,'w')
    t = float(tot)

    for line in f:
        v = line.rstrip().split()
        l = v[0]+" "+str(float(v[1])/t)+" "+str(float(v[2])/t)+"\n"
        o.write(l)
        

if __name__ == "__main__":
    eva = sys.argv[1] # list of IDs and E-value calculated for the entire sequence and for the best scoring domain 
    tot = sys.argv[2] # Number of sequences in the dataset
    out = sys.argv[3] # Output file 

    normalizator(eva,tot,out)