#!/usr/bin/python

############ SCRIPT ##############
# This script sort the IDs in clusters generated through the blastclust program according to their resolution  

import sys

# Function that create a dictionary containing IDs (key): resolution (value)
def get_dict(filename, p1 = 0, pv = -1): # p1: column of the ID; pv: column of the resolution 
    d = {}
    f = open(filename)
    for line in f:
        v = line.rstrip().split()
        d[v[p1]] = float(v[pv]) 
    return d

# Function that order the assign to each ID the resolution and sort the ID in the clust  
def sort_cluster(clist,d): # clist is the list of the ID in a specific cluster 
    tlist = []
    
    for pid in clist: # pid: protein ID 
        v = d.get(pid,float("inf")) # if the key is not present in the initial research (d) assign to it a resolution = to inf
        tlist.append([v,pid]) # v will contain the resolution and the ID 
    tlist.sort()
    return tlist 


if __name__ == "__main__":
    f1 = sys.argv[1] # file containing the cluster 
    f2 = sys.argv[2] # pdbsearch.txt --> file cointaining the ID and the resolution of each entry
    d = get_dict(f2) 
    
    f = open(f1)
    for line in f:
        lid = line.rstrip().split() # lid contains in each line the list of the ID of a different cluster
        slid = sort_cluster(lid,d) 

        s = ''
        for i in slid:
            s = s+i[1]+':'+str(i[0])+' '
        print len(slid), s





