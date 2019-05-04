#!/usr/local/bin/python3

############ SCRIPT ##############
# Given in input a list of IDs to this script it is able to extract their fasta sequences from a database  


import sys 

# Function to extract the fasta sequence of each ID 
def extract_seq (db, ID_list, out_file):
    ID_set = []
    out = open(out_file,'w')
    flag = 0   
    db_in = open(db) 
    ID = open(ID_list)

    for line_id in ID:
        ID_set.append(line_id.rstrip())

    for line in db_in:    
        if line[0] == '>':
            if (line.split()[0][1:] in ID_set):
                out.write(line)

                # Eliminate the ID from the list 
                ind = ID_set.index(line.split()[0][1:]) 
                ID_set.pop(ind)

                flag = 1
            else:
                flag = 0

        elif flag == 1:
                out.write(line)

    out.close()
    ID.close()
    db_in.close()


if __name__ == "__main__":
    ID_list = sys.argv[1] # File containing the list of IDs 
    db = sys.argv[2] # Database 
    out = sys.argv[3] # Output file 

    extract_seq (db, ID_list, out)