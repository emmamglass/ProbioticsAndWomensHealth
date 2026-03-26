import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def sort_by_frequency(lst):
	freq_dict = {}

	for element in lst:
		if element in freq_dict:
			freq_dict[element] += 1
		else:
			freq_dict[element] = 1

	sorted_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))
	sorted_list = []

	return sorted_dict

unique_commensal = pd.read_csv('Unique_commensal_anno.csv')
unique_pathogen = pd.read_csv('Unique_pathogen_anno.csv')
unique_probiotic = pd.read_csv('Unique_probiotic_anno.csv')

commensal_annot = unique_commensal['Annotation']
pathogen_annot = unique_pathogen['Annotation']
probiotic_annot = unique_probiotic['Annotation']

commensal_annot = commensal_annot.to_list()
commensal_annot = [x for x in commensal_annot if str(x) != 'nan']
commensal_annot = sort_by_frequency(commensal_annot)

pathogen_annot = pathogen_annot.to_list()
pathogen_annot = [x for x in pathogen_annot if str(x) != 'nan']
pathogen_annot = sort_by_frequency(pathogen_annot)

probiotic_annot = probiotic_annot.to_list()
probiotic_annot = [x for x in probiotic_annot if str(x) != 'nan']
probiotic_annot = sort_by_frequency(probiotic_annot)

fig, ax = plt.subplots(3,1)

commensal_annot_values = list(commensal_annot.values())
'''commensal_percent_subsystem = []
for value in PC_annot_values:
	percent = (int(value)/sum(PC_annot.values()))*100
	PC_percent_subsystem.append(percent)'''

ax[0].barh(np.arange(len(commensal_annot.keys())),commensal_annot_values, edgecolor='black', color = '#167DCC')
'''for label in ax[0].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')'''
#ax[0].set_title('Pathogen / Commensal Comparison')
#ax[0].set_title('Unique Commensal Reaction Subsystems')
#ax[0].set_ylabel('Metabolic subsystem')
ax[0].set_xlabel('Number of Reactions Unique to Commensals')
ax[0].set_yticks(np.arange(len(commensal_annot.keys())), commensal_annot.keys())
#plt.xticks(rotation=45, ha='right')


pathogen_annot_values = list(pathogen_annot.values())
'''PP_percent_subsystem = []
for value in PP_annot_values:
	percent = (int(value)/sum(PP_annot.values()))*100
	PP_percent_subsystem.append(percent)'''

ax[1].barh(np.arange(len(pathogen_annot.keys())),pathogen_annot_values, edgecolor='black', color = '#E4A358')
'''for label in ax[1].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')'''
#ax[1].set_title('Unique Pathogen Reactions')
#plt.xticks(rotation=45, ha='right')
#ax[1].set_title('Unique Pathogen Reaction Subsystems')
ax[1].set_xlabel('Number of Reactions Unique to Pathogens')
#ax[1].set_ylabel('Metabolic Subsystem')
ax[1].set_yticks(np.arange(len(pathogen_annot.keys())), pathogen_annot.keys())



probiotic_annot_values = list(probiotic_annot.values())
'''CP_percent_subsystem = []
for value in CP_annot_values:
	percent = (int(value)/sum(CP_annot.values()))*100
	CP_percent_subsystem.append(percent)'''

ax[2].barh(np.arange(len(probiotic_annot.keys())),probiotic_annot_values, edgecolor='black', color='#3C7F4D')
'''for label in ax[2].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')'''
#ax[2].set_title('Unique Probiotic Subsystems')
ax[2].set_xlabel('Number of Reactions Unique to Probiotics')
#ax[2].set_ylabel('Metabolic Subsystem')
ax[2].set_yticks(np.arange(len(probiotic_annot.keys())), probiotic_annot.keys())
#plt.xticks(rotation=45, ha='right')'''



plt.show()