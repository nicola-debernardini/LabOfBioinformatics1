SHELL := /bin/bash 

############ MAKEFILE: #############
# This makefile generate a list of non redundant PDB IDs selected according to their resolution 
# The results of this pipeline will be use to compute a multiple sequence alignment using PDBeFold (http://www.ebi.ac.uk/msd-srv/ssm/)


############ REQUIREMENTS: ##############

# Files:
# - Result of a PDBeFold search (PDBeFold_search.txt)
# - Result of a PDB search (pdbsearch.txt)

# Scripts:
ORD_CLUST = python ../../Scripts/ClustID_resol.py  # Script that order the ID in a clust according to their resolution 
FASTA_EXTRAC = python ../../Scripts/Extract_ProtSeq_PDB.py  # Script that give a list od ID extract their fasta sequence from the PDB_seqres.db 

# Databases:
# The precise release of the PDB database used is Apr 30_2019.
# The user must download the database since its size is too large to be uploaded on Github 
DB := ../db/pdb_seqres.db 


# Blastclust parameters:
COVERAGE =95
IDENTITY =99

########################################



# Objective:
OBJ := candidate_c$(COVERAGE)_s$(IDENTITY).ID

all: $(OBJ)

# Extract from each clusater the ID of the entry with the highest resolution 
candidate_c$(COVERAGE)_s$(IDENTITY).ID: candidate_c$(COVERAGE)_s$(IDENTITY).sorted
	@echo "------------------------------------------"
	cut -d " " -f 2 $^ | awk -F ":" '{print $$1}' > $@
	@echo

# Order the ID in the clusters according to the resolution of each entry
candidate_c$(COVERAGE)_s$(IDENTITY).sorted: candidate_c$(COVERAGE)_s$(IDENTITY).clust pdbsearch.list
	@echo "------------------------------------------"
	$(ORD_CLUST) $< <(sed 's/:/_/g' pdbsearch.list) > $@
	@echo

# Cluster of the candidate according to the seq ID and coverage
candidate_c$(COVERAGE)_s$(IDENTITY).clust: candidateID.fasta
	@echo "------------------------------------------"
	blastclust -i $^ -o $@ -L 0.$(COVERAGE) -S $(IDENTITY) 
	@echo

# Extract the fasta sequences of the candidates  
candidateID.fasta: candidateID.list $(DB)
	@echo "------------------------------------------"
	$(FASTA_EXTRAC) $^ $@
	@echo

# Generate a list of IDs of candidate entries that can be use to generate the HMM 
candidateID.list: PDBeFold_search.list pdbsearch.list
	@echo "------------------------------------------"
	comm -12 $< <(cut -d " " -f 1 pdbsearch.list) | sed 's/:/_/g' > $@
	@echo

# Extract the PDB ID of the entries returned by the PDBeFold search 
PDBeFold_search.list: PDBeFold_search.txt
	@echo "------------------------------------------"
	awk '{print tolower($$NF)}' $^ | awk -F ":" '{print $$1":"toupper($$2)}' | tail -n +2 | sort > $@
	@echo

# Extract the PDB ID of the entries returned by the PDB search
# Pay attention: the experimental methond must be "X-RAY DIFFRACTION"
pdbsearch.list: pdbsearch.txt
	@echo "------------------------------------------"
	cut -d "," -f 1,2,4,6 $^ | tail -n +2 | sed 's/"//g' | sed -e 's/,/ /g' | grep -v "^$$" | awk -F " " '{print tolower($$1)":"$$2" "$$3}' | sort > $@
	@echo

.PHONY: all clean

clean:
	rm -f *.list *.clust *.fasta *.sorted