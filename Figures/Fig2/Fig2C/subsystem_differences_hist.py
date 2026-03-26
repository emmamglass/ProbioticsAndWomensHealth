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

pathogen_commensal = pd.read_csv('Pathogens_Commensals_annot.csv')
pathogen_probiotic = pd.read_csv('Probiotic_Pathogen_annot.csv')
commensal_probiotic = pd.read_csv('Probiotic_Commensal_annot.csv')

PC_annot = pathogen_commensal['Annotation']
PP_annot = pathogen_probiotic['Annotation']
CP_annot = commensal_probiotic['Annotation']

PC_annot = PC_annot.to_list()
PC_annot = [x for x in PC_annot if str(x) != 'nan']
PC_annot = sort_by_frequency(PC_annot)

PP_annot = PP_annot.to_list()
PP_annot = [x for x in PP_annot if str(x) != 'nan']
PP_annot = sort_by_frequency(PP_annot)

CP_annot = CP_annot.to_list()
CP_annot = [x for x in CP_annot if str(x) != 'nan']
CP_annot = sort_by_frequency(CP_annot)



fig, ax = plt.subplots(1,3)

PC_annot_values = list(PC_annot.values())
PC_percent_subsystem = []
for value in PC_annot_values:
	percent = (int(value)/sum(PC_annot.values()))*100
	PC_percent_subsystem.append(percent)

ax[0].bar(PC_annot.keys(),PC_percent_subsystem, edgecolor='black')
for label in ax[0].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')
ax[0].set_title('Pathogen / Commensal Comparison')
ax[0].set_ylabel('Percent of Total Reactions')
#plt.xticks(rotation=45, ha='right')


PP_annot_values = list(PP_annot.values())
PP_percent_subsystem = []
for value in PP_annot_values:
	percent = (int(value)/sum(PP_annot.values()))*100
	PP_percent_subsystem.append(percent)

ax[1].bar(PP_annot.keys(),PP_percent_subsystem, edgecolor='black')
for label in ax[1].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')
ax[1].set_title('Pathogen / Probiotic Comparison')
#plt.xticks(rotation=45, ha='right')



CP_annot_values = list(CP_annot.values())
CP_percent_subsystem = []
for value in CP_annot_values:
	percent = (int(value)/sum(CP_annot.values()))*100
	CP_percent_subsystem.append(percent)

ax[2].bar(CP_annot.keys(),CP_percent_subsystem, edgecolor='black')
for label in ax[2].get_xticklabels():
  label.set_rotation(45)
  label.set_ha('right')
ax[2].set_title('Commensal / Pathogen Comparison')
#plt.xticks(rotation=45, ha='right')'''



plt.show()
