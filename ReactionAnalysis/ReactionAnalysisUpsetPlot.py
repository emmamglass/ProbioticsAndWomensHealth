import upsetplot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import from_memberships
from upsetplot import plot
from upsetplot import UpSet

Probiotic_df = pd.read_csv('Probiotic_rxn_anno.csv')
Pathogen_df = pd.read_csv('Pathogen_rxn_anno.csv')
Commensal_df = pd.read_csv('Commensal_rxn_anno.csv')

Probiotic_rxns = Probiotic_df['Reaction']
Pathogen_rxns = Pathogen_df['Reaction']
Commensal_rxns = Commensal_df['Reaction']

Probiotic_Pathogen = list(set(Probiotic_rxns)&set(Pathogen_rxns))
Probiotic_Commensal = list(set(Probiotic_rxns)&set(Commensal_rxns))
Pathogen_Commensal = list(set(Pathogen_rxns)&set(Commensal_rxns))
Probiotic_Pathogen_Commensal = list(set(Probiotic_rxns)&set(Pathogen_rxns)&set(Commensal_rxns))

upset_data = from_memberships([['Commensal'], ['Pathogen'], ['Probiotic'],
							   ['Commensal', 'Pathogen'], ['Commensal', 'Probiotic'], ['Pathogen', 'Probiotic'],
							   ['Commensal', 'Pathogen', 'Probiotic']],
							   data = [len(Commensal_rxns), len(Pathogen_rxns), len(Probiotic_rxns),
							           len(Pathogen_Commensal), len(Probiotic_Commensal), len(Probiotic_Pathogen),
							           len(Probiotic_Pathogen_Commensal)])
c = [element for element in Pathogen_rxns if element not in Pathogen_Commensal]
d = [element for element in Probiotic_rxns if element not in Probiotic_Commensal]
e = [element for element in Probiotic_rxns if element not in Probiotic_Pathogen]
print('Pathogen/commensal' + str(c))
print('Probiotic/commensal' + str(d))
print('probiotic/pathogen' + str(e))

#print(len(Commensal_rxns), len(Pathogen_rxns), len(Probiotic_rxns),
#							           len(Pathogen_Commensal), len(Probiotic_Commensal), len(Probiotic_Pathogen),
#							           len(Probiotic_Pathogen_Commensal))

UpSet(upset_data, show_counts=True).plot()
plt.show()