import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('PubMed_Probiotics_Timeline_Results_by_Year.csv')
plt.plot(data['Year'], data['Count'], c = "#3C7F4D", linewidth=4)
plt.xlabel('Year', fontsize = 12)
plt.ylabel('Number of "Probiotics"\n Pubmed Articles', fontsize = 12)
plt.show()