SHELL := /bin/bash 

############ MAKEFILE: #############
# This makefile generate the HMM and measure the preformance of the predictor 


############ REQUIREMENTS: ##############

# Files:
# - List of the training set ID (candidate_c$(COVERAGE)_s$(IDENTITY).ID)
# - Multiple structure alignment of the entry that will be use to train the HMM (stru_align.sto)
# - ID of the entire positive set (positive.list)
# - ID of the entire negative set (NonKunitz.list)

# Python script:
EXTRA_UNI_FASTA = python ../Scripts/Extrac_fasta.py
EXTRA_PDB_FASTA = python ../Scripts/Extract_ProtSeq_PDB.py
CONFUS_MATRIX = python ../Scripts/CM_nice.py
TRAIN_MODEL = python ../Scripts/Set_model_parameters.py
NORMALIZER = python ../Scripts/Normalized_eva.py
ROC_CURVE = python ../Scripts/ROC_curve.py

# Database:
DB_UNI := ../db/uniprot_sprot.fasta
DB_PDB := ../db/pdb_seqres.db

##########################################


# Objective:
OBJ := model_perform_1half.txt model_perform_2half.txt

all: $(OBJ)

#################################
# Optimization and Performances #
#################################

# Calculate the overall performance of the model:
performance.txt: def_1half.eva def_2half.eva set_model_2half.txt set_model_1half.txt
	@echo "------------------------------------------"
	cat def_1half.eva def_2half.eva > definitive.tmp
	$(CONFUS_MATRIX) definitive.tmp $$(grep '>' set_model_2half.txt | awk -F " " '{print $$6}') $$(grep '>' set_model_1half.txt | awk -F " " '{print $$6}') > $@
	$(ROC_CURVE) definitive.tmp
	@echo
	
# Calculate the performance of the model on the 1half set:
model_perform_1half.txt: set_model_2half.txt def_1half.eva
	@echo "------------------------------------------"
	$(CONFUS_MATRIX) def_1half.eva $$(grep '>' $< | awk -F " " '{print $$6}') > $@
	@echo

# Calculate the best parameter of the model for the 2half:
set_model_2half.txt: def_2half.eva def_1half.eva 
	@echo "------------------------------------------"
	$(TRAIN_MODEL) def_2half.eva > $@
	#$(ROC_CURVE) def_2half.eva
	@echo

# Calculate the performance of the model on the 2half set:
model_perform_2half.txt: set_model_1half.txt def_2half.eva
	@echo "------------------------------------------"
	$(CONFUS_MATRIX) def_2half.eva $$(grep '>' $< | awk -F " " '{print $$6}') > $@
	@echo	

# Calculate the best parameter of the model for the 1half:
set_model_1half.txt: def_1half.eva def_2half.eva
	@echo "------------------------------------------"
	$(TRAIN_MODEL) def_1half.eva > $@
	#$(ROC_CURVE) def_1half.eva
	@echo


#################################
# 2-fold cross validation sets  #
#################################

# Create the complete list of pos and neg ID and E-value cassified respectively with 1 and 2
def_2half.eva: negative_2half.eva positive_2half.eva
	@echo "------------------------------------------"
	awk '{print $$0, "1"}' positive_2half.eva > positive_2half.compl
	cat positive_2half.compl $< > $@
	@echo

# Create the complete list of pos and neg ID and E-value cassified respectively with 1 and 2
def_1half.eva: negative_1half.eva positive_1half.eva
	@echo "------------------------------------------"
	awk '{print $$0, "1"}' positive_1half.eva > positive_1half.compl
	cat positive_1half.compl $< > $@
	@echo


###############################
# E-value of the negative set #
###############################

# Generate the list of the negative 2half set ID and E-value classified with a 2: 
negative_2half.eva: negative_2half.fasta pre_negative_2half.eva
	@echo "------------------------------------------"
	comm -23 <(grep '>' $< | awk -F "|" '{print $$2}' | sort) <(awk -F "|" '{print $$2}' pre_negative_2half.eva | sort) > missing_2half.tmp 
	cat <(awk '{print $$0, "2"}' pre_negative_2half.eva) <(awk '{print "sp|"$$0"|MANCANTE", "1.0 1.0 2"}' missing_2half.tmp) > $@
	@echo

# Generate the list of the negative 1half set set ID and E-value classified with a 2: 
negative_1half.eva: negative_1half.fasta pre_negative_1half.eva
	@echo "------------------------------------------"
	comm -23 <(grep '>' $< | awk -F "|" '{print $$2}' | sort) <(awk -F "|" '{print $$2}' pre_negative_1half.eva | sort) > missing_1half.tmp 
	cat <(awk '{print $$0, "2"}' pre_negative_1half.eva) <(awk '{print "sp|"$$0"|MANCANTE", "1.0 1.0 2"}' missing_1half.tmp) > $@
	@echo

# Assign a score to the alignment between the hmm and the sequences of the 2half set
pre_negative_2half.eva: model.hmm negative_2half.fasta
	@echo "------------------------------------------"
	hmmsearch --domE 600000 -E 600000 --max --noali -o negative_2half.hsearch $^
	tail -n +19 negative_2half.hsearch | awk 'BEGIN {flag = 0} {if(flag == 0 && $$0 !~/^$$/) {print $$0} else flag = 1}' | cut -b 1-87 | awk '{print $$NF, $$1, $$4}' | grep '^sp' > evaneg_2half.tmp
	$(NORMALIZER) evaneg_2half.tmp $$(echo $$(grep -c '>sp' negative_2half.fasta | cut -d " " -f 1)) $@
	@echo

# Assign a score to the alignment between the hmm and the sequences of the 1half set 
pre_negative_1half.eva: model.hmm negative_1half.fasta
	@echo "------------------------------------------"
	hmmsearch --domE 600000 -E 600000 --max --noali -o negative_1half.hsearch $^
	tail -n +19 negative_1half.hsearch | awk 'BEGIN {flag = 0} {if(flag == 0 && $$0 !~/^$$/) {print $$0} else flag = 1}' | cut -b 1-87 | awk '{print $$NF, $$1, $$4}' | grep '^sp' > evaneg_1half.tmp
	$(NORMALIZER) evaneg_1half.tmp $$(echo $$(grep -c '>sp' negative_1half.fasta | cut -d " " -f 1)) $@
	@echo

# Divide the sequences of the negative sets randomly in two: a 1half set and a 2half set  
negative_1half.fasta negative_2half.fasta: negative.fasta 
	@echo "------------------------------------------"
	cat negative.fasta | tr -d '\n' | sed 's/>sp/\n>sp/g' | sort -R | head -n +$$(echo $$(grep -c '>sp' negative.fasta) "/2" | bc ) > tmp_neg_1half.fasta
	comm -23 <(cat negative.fasta | tr -d '\n' | sed 's/>sp/\n>sp/g' | sort) <(sort tmp_neg_1half.fasta) > tmp_neg_2half.fasta
	sed 's/SV=[[:digit:]]/&\n/g' tmp_neg_1half.fasta > negative_1half.fasta
	sed 's/SV=[[:digit:]]/&\n/g' tmp_neg_2half.fasta > negative_2half.fasta
	@echo


###############################
# E-value of the positive set #
###############################

# Assign a score to the alignment between the HMM and the sequences of the positive 2half set 
positive_2half.eva: model.hmm positive_2half.fasta
	@echo "------------------------------------------"
	hmmsearch --max --noali -o positive_2half.hsearch $^
	tail -n +18	positive_2half.hsearch | awk 'BEGIN {flag = 0} {if(flag == 0 && $$0 !~/^$$/) {print $$0} else flag = 1}' | cut -b 1-83 | awk '{print $$NF, $$1, $$4}' | grep '^sp' > evapos_2half.tmp
	$(NORMALIZER) evapos_2half.tmp $$(echo $$(grep '>sp' positive_2half.fasta | wc -l | cut -d " " -f 1)) $@
	@echo 

# Assign a score to the alignment between the HMM and the sequences of the positive 1half set 
positive_1half.eva: model.hmm positive_1half.fasta
	@echo "------------------------------------------"
	hmmsearch --max --noali -o positive_1half.hsearch $^
	tail -n +18	positive_1half.hsearch | awk 'BEGIN {flag = 0} {if(flag == 0 && $$0 !~/^$$/) {print $$0} else flag = 1}' | cut -b 1-83 | awk '{print $$NF, $$1, $$4}' | grep '^sp' > evapos_1half.tmp
	$(NORMALIZER) evapos_1half.tmp $$(echo $$(grep '>sp' positive_1half.fasta | wc -l | cut -d " " -f 1)) $@
	@echo 

# Divide the sequences of the positive sets randomly in two: a 1half set and a 2half set   
positive_1half.fasta positive_2half.fasta: def_posit.fasta 
	@echo "------------------------------------------"
	cat def_posit.fasta |tr -d '\n' | sed 's/>sp/\n>sp/g' | sort -R | head -n $$(echo $$(grep -c '>sp' def_posit.fasta) "/2" | bc ) > tmp_pos_1half.fasta
	comm -23 <(cat def_posit.fasta | tr -d '\n' | sed 's/>sp/\n>sp/g' | sort) <( sort tmp_pos_1half.fasta) > tmp_pos_2half.fasta
	sed 's/SV=[[:digit:]]/&\n/g' tmp_pos_1half.fasta > positive_1half.fasta
	sed 's/SV=[[:digit:]]/&\n/g' tmp_pos_2half.fasta > positive_2half.fasta
	@echo

# Extract the sequences in fasta format of the definitive positive format  
def_posit.fasta: def_posit.txt $(DB_UNI)
	@echo "------------------------------------------"
	$(EXTRA_UNI_FASTA) $^ $@
	@echo


################
# Positive set #
################

# Finally create the positive set: 
def_posit.txt: positive.list WhatToRemove.txt
	@echo "------------------------------------------"
	comm -23 <(sort $<) WhatToRemove.txt > $@ 
	@echo "There final number of Uniprot entries in the positive set are: " $$(wc -l $@)
	@echo 

# Define which are the sequences to be remove from the positive set because 'too simple' (thus already present in the training set):
WhatToRemove.txt: blast.txt
	@echo "------------------------------------------"
	awk '{if ($$3==100) print $$1,$$2,$$3,$$11}' $^ | awk -F "|" '{print $$2}' | sort -u > $@ 
	@echo "There are N Uniprot entry to remove: " $$(wc -l $@)
	@echo

# Find through a blast search the seq identity between the proteins of the two sets: 
blast.txt: training.fasta positive.fasta
	# In order to be able to run blast I need to index the database:
	formatdb -i positive.fasta -p T

	blastall -p blastp -i $< -d positive.fasta -m 8 -o $@

# Extract the fasta sequences of the training ID set from the PDB database:
training.fasta: candidate_c95_s99.ID $(DB_PDB)
	$(EXTRA_PDB_FASTA) $^ $@

# Extract the fasta sequences of the possitive ID set:
positive.fasta: positive.list $(DB_UNI)
	$(EXTRA_UNI_FASTA) $^ $@


###############
# HMM Profile #
###############

# Built the HMM model starting from the multiple sequence alignment of the proteine in the training set:
model.hmm: stru_align.sto
	hmmbuild $@ $<


################
# Negative set #
################

# Extract the fasta sequences of the negative ID set:
negative.fasta: negative.list $(DB_UNI) 
	$(EXTRA_UNI_FASTA) $^ $@

# Extract in a random way from the entire negative ID set a number of IDs  
# negative.list: NonKunitz.list
#	sort -R $< | head -n $(NUM_RAND) > $@ 

.PHONY: all clean

clean:
	rm -f *.fasta *.hmm *.txt *.eva *.hsearch *.tmp