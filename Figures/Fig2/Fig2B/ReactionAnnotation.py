import numpy as np
import pandas as pd
import os
import cobra
from cobra.io import read_sbml_model
import re
import requests
import pandas as pd
from Bio import SeqIO
from Bio.KEGG import REST
from Bio.KEGG.KGML import KGML_parser

def annotate_reactions(input_filename, output_filename):
	with open(input_filename) as f:
		lines = [line.rstrip('\n').replace('_c','').replace('_e','') for line in f]
	#generate dictionary of reaction names
	all_reaction_dict = dict.fromkeys(lines)

	#Query the modelseed db
	r = requests.get("https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/reactions.tsv")
	r = r.content.decode("utf-8")

	count = 0

	for key in all_reaction_dict:
		annotations = r
		present = annotations.find(key)
		if present != -1:
			right = annotations[present:]
			position = right.find("KEGG: ")
			if position != -1:
				all_reaction_dict[key] = right[position+6:position+13]
			elif position == -1:
				all_reaction_dict[key] = "NA"
		elif present == -1:
			all_reaction_dict[key] = "NA"
		#print(count)
		count+=1
	clean_dict = {key.strip("|"): item.strip("|") for key, item in all_reaction_dict.items()}


	count = 0
	for key, value in clean_dict.items():
		try:
			kegg = REST.kegg_get(value).read()
			position = kegg.find("Metabolism; ")
			if position != -1:
				clean_dict[key] = re.search('Metabolism;(.*)\n', kegg)
			elif position == -1:
				clean_dict[key] = "NA"
			print(clean_dict[key])
		except:
			pass
		print(count)
		count +=1

	with open(output_filename, 'w') as f:
		count = 0
		for key in clean_dict.keys():
			f.write("%s,%s\n"%(key,clean_dict[key]))
			print(count)
			count +=1

if __name__=="__main__":
	annotate_reactions('Unique_commensal_rxns.txt','Unique_commensal_anno.csv')
	annotate_reactions('Unique_probiotic_rxns.txt','Unique_probiotic_anno.csv')
	annotate_reactions('Unique_pathogen_rxns.txt','Unique_pathogen_anno.csv')
	#annotate_reactions('Probiotic_rxns.txt', 'Probiotic_rxn_anno.csv')
	#annotate_reactions('Pathogen_rxns.txt', 'Pathogen_rxn_anno.csv')
	#annotate_reactions('Commensal_rxns.txt', 'Commensal_rxn_anno.csv')








