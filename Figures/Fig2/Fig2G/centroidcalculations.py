import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import cdist
from matplotlib.patches import Ellipse
from scipy.stats import kruskal

# Load the dataset
file_path = "data_to_plot.csv"
df = pd.read_csv(file_path)

# Ensure proper column names (adjust based on actual column names in CSV)
classification_col = "Classification"
component_cols = ["Component 1", "Component 2"]

# Define custom classification order
'''classification_order = ["Lactobacillus gasseri", "Lactococcus plantarum", "Bacillus subtilis", 
                        "Lacticaseibacillus rhamnosus GG", "Bifidobacterium animalis I", 
                        "Lactococcus lactis", "Lactobacillus helveticus", "Bifidobacterium animalis II", 
                        "Akkermansia muciniphila", "Bifidobacterium bifidum", "Limosilactobacillus fermentum I",
                        "Lactobacillus brevis", "Lactobacillus delbrueckii", "Bifidobacterium breve", 
                        "Lactobacillus reuteri", "Lactobacilllus acidophilus", "Bacillus clausii",
                        "Bifidobacterium longum", "Bacillus coagulans", "Lacticaseibacillus rhamnosus",
                        "Pediococcus pentosaceus", "Lactobacillus rhamnosus", "Limosilactobacillus reuteri",
                        "Limosilactobacillus fermentum II", "Bacillus infantis",
                        "Lactobacillus casei", "Lactobacillus johnsonii", "Lactobacillus crispatus",
                        "Streptococcus thermophilus", "Lactiplantibaciulls plantarum", "Bifidobacterium adolescentis",
                        "Enterococcus faecium", "Ligilactobacillus salivarius", "Pediococcus acidilactici"]'''

classification_order = ['Lactobacillaceae', 'Streptococcaceae', 'Bacillaceae', 'Bifidobacteriaceae',
                        'Akkermansiaceae', 'Enterococcaceae']
df[classification_col] = pd.Categorical(df[classification_col], categories=classification_order, ordered=True)

# Sort dataframe based on classification order
df = df.sort_values(by=classification_col)

# Compute centroids for each classification
centroids = df.groupby(classification_col)[component_cols].mean().reset_index()

# Compute standard deviation of each point from its classification centroid
df = df.merge(centroids, on=classification_col, suffixes=("", "_centroid"))
df["Distance from Centroid"] = np.linalg.norm(
    df[component_cols].values - df[[f"{c}_centroid" for c in component_cols]].values, axis=1
)

# Compute standard deviation of distances within each classification
std_devs = df.groupby(classification_col)["Distance from Centroid"].std()

# Compute covariance matrices for ellipses
cov_matrices = df.groupby(classification_col)[component_cols].cov().groupby(level=0).apply(np.array)


# Display results
print("Centroids:\n", centroids)
print("\nStandard Deviations:\n", std_devs)

'''# create palette
palette = {
    "Commensal": "#167dcc",
    "Pathogen": "#e4a358",
    "Probiotic": "#3c7f4d"
}'''

# Get the color palette from seaborn
palette = dict(zip(classification_order, sns.color_palette("Spectral", n_colors=len(classification_order))))

# Create the scatter plot
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(data=df, x="Component 1", y="Component 2", hue=classification_col, palette=palette, alpha=.6, edgecolor='black')


# Plot each centroid and ellipse with the corresponding color f
ax = plt.gca()
for _, row in centroids.iterrows():
    class_name = row[classification_col]
    centroid_x, centroid_y = row["Component 1"], row["Component 2"]
    color = palette[class_name]
    
    # Draw confidence ellipse
    if class_name in cov_matrices:
        cov = cov_matrices[class_name]
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        
        # Width and height of ellipse based on eigenvalues (scaled by standard deviation)
        width, height = 2 * 2*  np.sqrt(eigenvalues)  # 1 std dev ≈ 68% of points, multipy by 2 for 2 standard deviations
        angle = np.degrees(np.arctan2(*eigenvectors[:, 0][::-1]))  # Convert to degrees
        
        ellipse = Ellipse((centroid_x, centroid_y), width, height, angle, edgecolor='black', facecolor='none', linestyle="-", linewidth=2)
        ax.add_patch(ellipse)

        ellipse = Ellipse((centroid_x, centroid_y), width, height, angle, edgecolor=color, facecolor='none', linestyle="-", linewidth=1)
        ax.add_patch(ellipse)

for _, row in centroids.iterrows():
    class_name = row[classification_col]
    centroid_x, centroid_y = row["Component 1"], row["Component 2"]
    color = palette[class_name]

    # Scatter centroid
    plt.scatter(centroid_x, centroid_y, color=color, marker='^', s=150, edgecolors='black', label=f"{class_name} Centroid")
    
# Ensure the legend is correctly handled
handles, labels = plt.gca().get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
plt.legend(unique_labels.values(), unique_labels.keys(), fontsize = 7, bbox_to_anchor=(1.05, 1), loc="upper left")

# Compute the median distance between centroids for each classification
distances_by_class = []

# Group centroids by classification and compute pairwise distances
for class_name in classification_order:
    # Get the centroid of the current classification
    centroid = centroids[centroids[classification_col] == class_name][component_cols].values.flatten()
    
    # Compute the distance of each point from this centroid
    distances = np.linalg.norm(df[df[classification_col] == class_name][component_cols].values - centroid, axis=1)
    
    # Add these distances to the list (grouped by classification)
    distances_by_class.append(distances)

# Perform Kruskal-Wallis test on the median distances
stat, p_value = kruskal(*distances_by_class)

# Display results
print(f"Kruskal-Wallis Test for Median Distances Between Centroids:")
print(f"H-statistic = {stat}, p-value = {p_value}")

# Interpret the results
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is significant clustering (reject null hypothesis).")
else:
    print("There is no significant clustering (fail to reject null hypothesis).")



plt.show()