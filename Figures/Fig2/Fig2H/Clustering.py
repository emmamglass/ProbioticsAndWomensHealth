import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
import os 
import seaborn as sns
import glob
from mycolorpy import colorlist as mcp
import numpy as np

#takes gapsplit .csv output, downsamples, does pca, 
#returns tansformed pca object with data labels

def cluster(clustertype='pca', downsample=500):
	#empty df to store data from files
	combined_df = pd.DataFrame()

	#empty list to store filenames/labels
	filename_list = []

	#empty list to store classification
	classification_list = []

	#iterating through files, getting data to dataframe
	i=0
	for file in glob.glob('*.sbml.csv'):
		print(file)
		i+=1
		flux_df = pd.read_csv(file)

		#downsampling dataframe if necessary
		if downsample != 500:
				flux_df = flux_df.sample(n=downsample)

		#combining dataframes
		combined_df = pd.concat([combined_df, flux_df], axis=0)

		#adding file name to dataframe
		for n in range(downsample):
			filename_list.append(str(file))

		with open('probiotics_flux_list.txt') as f:
			if str(file) in f.read():
				classification = str('Probiotic')
			else:
				with open('pathogens_flux_list.txt') as f:
					if str(file) in f.read():
						classification = str('Pathogen')
					else: 
						classification = str('Commensal')

		for n in range(downsample):
			classification_list.append(classification)

	#converting filename labels to a series obj
	filename_df = pd.Series((v for v in filename_list), name = 'Label')

	#converting classification label to a series obj
	classification_df = pd.Series((v for v in classification_list), name = 'Classification')

	#convert dataframe to numpy array
	flux_array = combined_df.to_numpy()
	flux_array = np.nan_to_num(flux_array)

	if clustertype == 'kmeans':
		inertias = []
		for i in range(1,11):
			kmeans=KMeans(n_clusters=i)
			kmeans.fit(flux_array)
			inertias.append(kmeans.inertia_)
		plt.plot(range(1,11), inertias, marker='o')
		plt.title('Elbow method')
		plt.xlabel('Number of Clusters')
		plt.ylabel('Inertia')
		plt.show

	if clustertype == 'pca':
		#make pca object
		pca = PCA(n_components=2)

		#fit PCA object and transform array to 2D
		flux_array_transformed = pca.fit(flux_array).transform(flux_array)


		# Get the variance explained by PC1 and PC2
		variance_pc1 = pca.explained_variance_ratio_[0]
		variance_pc2 = pca.explained_variance_ratio_[1]

		print("pc1 variance is: ", variance_pc1)
		print("pc2 variance is: ", variance_pc2)



	if clustertype == 'tsne': 
		#make tsne object
		tsne = TSNE(n_components=2)

		#fit tsne object and transform array to 2D
		flux_array_transformed = tsne.fit(flux_array).fit_transform(flux_array)

	if clustertype == 'mds':
		#make distance object (we are going to use manhattan)
		distance = pairwise_distances(flux_array, metric = 'braycurtis')

		#make mds object 
		mds = MDS(n_components=2, dissimilarity = 'precomputed')

		#fit mds object and transform array to 2D
		flux_array_transformed = mds.fit(distance).fit_transform(distance)

	'''#convert to dataframe
	flux_df_transformed = pd.DataFrame(flux_array_transformed, columns=['Component 1', 'Component 2'])

	#Concat transformed data and labels
	data_to_plot = pd.concat([flux_df_transformed, filename_df, classification_df], axis = 1)
	data_to_plot.to_csv('data_to_plot.csv')
	return data_to_plot'''




if __name__ =='__main__':
	########making PCA plot#########
	#get transformed pca data and labels
	cluster_data = cluster('pca', 50)
	#print(cluster_data)
	#cluster_data.to_csv("ClusterData.csv", index=False)
	#print("saved csv")

	#num labels
	#num_labels = int(len(cluster_data['Classification'])/100)
	#targets = cluster_data['Classification'].unique()
	#colors = mcp.gen_color(cmap='gist_ncar',n=num_labels)
	#cluster_data = cluster_data.sort_values(by = ['Classification'], ascending=False )
	
	'''targets = ['Commensal','Pathogen', 'Probiotic']
	colors = ['#167DCC','#E4A358', '#3C7F4D']

	for target, color in zip(targets, colors):
		indicesToKeep = cluster_data['Classification'] == target
		plt.scatter(cluster_data.loc[indicesToKeep, 'Component 1'], cluster_data.loc[indicesToKeep,'Component 2'], c = color, alpha = 0.4, s = 30)
	

	cluster_data.to_csv("ClusterData.csv", index=False)
	print("saved csv")'''



	'''#define the color pallette
	color_labels = cluster_data['Label'].unique()
	col_values = sns.color_palette('tab10')
	color_map = dict(zip(color_labels, col_values))
	colors = [color_map[label] for label in cluster_data['Label'].values]
	
	

	#make scatterplot
	plt.scatter(cluster_data['Component 1'], cluster_data['Component 2'], c = colors)'''
	
	plt.show()


