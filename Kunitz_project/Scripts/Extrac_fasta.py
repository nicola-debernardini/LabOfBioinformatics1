#!/usr/bin/python

############ SCRIPT ##############
# Given in input a list of IDs to this script it is able to extract their fasta sequences from a database  


import sys

# Function to extract the fasta sequence of each ID 
def get_list_fasta(lid,fasta,out):
    f = open(fasta)
    o = open(out,'w')
    c = 0

    for line in f:
        line = line.rstrip()
        if line[0] == '>':
            tid = line.split('|')[1] # Uniprot fasta
            #tid = line.split()[0][1:] # PDB fasta

        if lid.get(tid,False):  # Check if the identifier is present in the dictionary or not 
            c = 1
        else:
            c = 0
        if c == 1:
            o.write(line+"\n")
    o.close()

if __name__ == "__main__":
        fid = sys.argv[1] # File containing the list of IDs
        fasta = sys.argv[2] # Database: Uniprot or PDB
        out = sys.argv[3] # Output file 

        lid = dict([(i,True)for i in open(fid).read().split('\n')]) # create a dictionary containing the IDs as keys
        get_list_fasta(lid,fasta,out)
        

