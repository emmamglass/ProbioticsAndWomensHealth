import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import braycurtis
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from colour import Color
from random import randint
import numpy as np

data = pd.read_csv('BinarySpeciesPresence.csv')
print(data)

name = data['Name']
brand = data['Brand']
general_use = data['Use (General)']
use = data['Use']
num_strains = data['Number of Strains'].astype(float)
num_species = data['Number of Species'].astype(float)

reduced_brand = pd.DataFrame(data=[data['Brand'],data['Number of Species']]).T
brands = ['CVS', 'Walgreens','Culturelle','Spring Valley','Garden of Life', 'Align', 'Florastor'
		  "Nature's Way", 'Equate', 'Renew Life', 'Digestive Advantage', 'Olly']
reduced_brand = reduced_brand[reduced_brand.Brand.isin(brands)]
print(reduced_brand)

PROPS = {'boxprops':{'facecolor':'#4A885A', 'edgecolor':'black'}, 'medianprops':{'color':'black'}, 'whiskerprops':{'color':'black'}, 'capprops':{'color':'black'}}
fig, ax = plt.subplots()
#sns.stripplot(data=reduced_brand, x=reduced_brand['Brand'], y=reduced_brand['Number of Species'], color = 'black', alpha = 0.5, jitter=True)
my_plot = sns.boxplot(ax=ax, data=reduced_brand, x = reduced_brand['Brand'], y = reduced_brand['Number of Species'], **PROPS)#color='gray', edgecolor='black', capsize=.3)# **PROPS)
my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
my_plot.set_xlabel('Brand of Probiotic Supplement')
plt.show()

fig, ax = plt.subplots()
my_plot = sns.histplot(ax=ax, data=data, x=num_species, bins = 20, binwidth=1, facecolor='#4A885A')
my_plot.set_xticks([1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5])
my_plot.set_xticklabels([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
my_plot.set_ylabel('Number of Probiotic Supplements')
plt.show()

### Binary species presence
binary_df = data.iloc[:,6:].fillna(0)
similarities = pairwise_distances(binary_df, metric = 'hamming')

binary_df_names = pd.concat([general_use,binary_df], axis=1)

pca = PCA(n_components=2)
mds = MDS(n_components=2, dissimilarity = 'precomputed')

result = pca.fit_transform(binary_df)
print(pca.explained_variance_ratio_, "Variance of each dimension")
#result = mds.fit_transform(similarities)
result = pd.DataFrame(result)

'''targets = ['CVS', 'Align', "Nature's Bounty", 'Florastor', "Garden of Life", 
		   'Culturelle', "Phillips'", "Nature Made", 'Olly', "Physician's Choice", "RePHresh",
		   'AZO', "Nature's Way", 'RenewLife', ' Benefiber', 'Digestive Advantage', 'Metamucil',
		   'Ombre', 'TruBiotics', 'goli', 'FRISKA', 'Terra Origin', 'GoodBelly', 'Codeage', 'Hers',
		   "Beekeeper's", 'Live Better', 'Walgreens', 'Florajen', 'New Chapter', 'up4', "Nature's Truth",
		   "Lifeable", 'BioSchwartz', 'Nutrition Now', 'Enzymatic Therapy', 'Cardiotabs', 'HerOwn',
		   'Irwin Naturals', "Mommy's Bliss", 'Vitafusion']'''

targets = ['Gut', 'Respriatory', 'Skin', 'Heart','Oral', 'Muscle', 'Bone', 'Vaginal/Urinary']
colors = ['#16629D', '#308C7B', '#D7AE3E', '#068B37', '#7E4C97', '#992B2E','#CA5D0A','#9AEDEC']

def rand_jitter(data):
	stdev = 0.01 *(data.max()-data.min())
	return data + np.random.randn(data.size)*stdev

def jitter(x, y, s=20, c='b', marker = 'o', cmap=None, norm=None, vmin = None, vmax = None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs):
	return plt.scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax = vmax, alpha = alpha, linewidths=linewidths, **kwargs)

'''colors = []
for i in range(41):
    colors.append('#%06X' % randint(0, 0xFFFFFF))'''

for target, color in zip(targets, colors):
	indicesToKeep = general_use == target
	jitter(result.loc[indicesToKeep,0], result.loc[indicesToKeep,1], c = color, alpha=.9, s=100, edgecolors='black')


plt.show()






