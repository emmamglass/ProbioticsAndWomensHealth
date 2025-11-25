# Commensal-Pathogen-Probiotic Clustering Analysis

This folder contains scripts for clustering and visualizing metabolic flux data from commensal, pathogenic, and probiotic bacteria.

## Files

### `Clustering.py`
**Purpose**: Performs dimensionality reduction and clustering on flux data from multiple bacterial species.

**Functionality**:
- Reads flux data from `.sbml.csv` files (output from gap-split flux sampling)
- Classifies species as Probiotic, Pathogen, or Commensal based on text files (`probiotics_flux_list.txt`, `pathogens_flux_list.txt`)
- Downsamples flux data (default: 500 samples per species)
- Performs dimensionality reduction using:
  - **PCA** (Principal Component Analysis) - default
  - **t-SNE** (t-distributed Stochastic Neighbor Embedding)
  - **MDS** (Multidimensional Scaling with Bray-Curtis distance)
  - **K-means** (for elbow method to determine optimal cluster number)
- Outputs variance explained by principal components (for PCA)
- Can save transformed data with labels to CSV

**Usage**:
```python
cluster_data = cluster('pca', downsample=50)
```

**Parameters**:
- `clustertype`: 'pca', 'tsne', 'mds', or 'kmeans'
- `downsample`: Number of flux samples per species (default: 500)

**Input Files Required**:
- `*.sbml.csv` - Flux sampling output files
- `probiotics_flux_list.txt` - List of probiotic species filenames
- `pathogens_flux_list.txt` - List of pathogen species filenames

**Output**:
- Transformed flux data with component coordinates
- Classification labels (Probiotic/Pathogen/Commensal)
- Variance explained statistics (for PCA)

---

### `centroidcalculations.py`
**Purpose**: Calculates and visualizes centroids and confidence ellipses for clustered data.

**Functionality**:
- Loads clustered data from `data_to_plot.csv`
- Computes centroids for each classification group (Commensal, Pathogen, Probiotic)
- Calculates distances from centroids for each data point
- Computes standard deviations and covariance matrices
- Draws confidence ellipses (2 standard deviations) around centroids
- Performs Kruskal-Wallis test to assess significance of clustering
- Creates scatter plot with color-coded groups and centroid markers

**Usage**:
```bash
python centroidcalculations.py
```

**Input Files Required**:
- `data_to_plot.csv` - Output from `Clustering.py` containing:
  - Component 1, Component 2 (PCA/t-SNE/MDS coordinates)
  - Classification (Commensal/Pathogen/Probiotic)

**Output**:
- Scatter plot with:
  - Color-coded points by classification
  - Centroid markers (triangles)
  - Confidence ellipses (2 SD)
- Statistical output:
  - Centroid coordinates
  - Standard deviations
  - Kruskal-Wallis test results

**Color Scheme**:
- Commensal: `#167dcc` (blue)
- Pathogen: `#e4a358` (orange)
- Probiotic: `#3c7f4d` (green)

---

### `flux_heatmap.py`
**Purpose**: Creates clustered heatmaps of median flux values across reactions, grouped by bacterial classification.

**Functionality**:
- Reads flux data from multiple CSV files
- Groups species into: Probiotic, Uninhibitory (vaginal commensals), Inhibitory (vaginal commensals), Gardnerella vaginalis
- Computes median flux per reaction for each species
- Filters reactions:
  - Removes low-variance reactions (variance < 0.1)
  - Removes highly correlated reactions (correlation > 0.9)
- Maps file names to species names using `file_species_mapping.csv`
- Maps reactions to subsystems using `all_reactions.csv`
- Creates clustered heatmap with:
  - Row colors indicating bacterial group
  - Column colors indicating metabolic subsystem
  - Hierarchical clustering using Canberra distance and average linkage

**Usage**:
```bash
python flux_heatmap.py
```

**Input Files Required**:
- `vaginal_probiotic.txt` - List of probiotic species filenames
- `uninhibitory_vag_comm.txt` - List of uninhibitory vaginal commensal filenames
- `inhibitory_vag_comm.txt` - List of inhibitory vaginal commensal filenames
- `gardnerella_vaginalis.txt` - List of Gardnerella vaginalis filenames
- `file_species_mapping.csv` - Mapping of filenames to species names
- `all_reactions.csv` - Mapping of reactions to subsystems
- Flux CSV files referenced in the text files above

**Output**:
- Clustered heatmap visualization
- `all_reactions.txt` - List of all reactions (before filtering)

**Color Scheme**:
- Row colors:
  - Probiotic: `#437a51` (green)
  - Commensal: `#095e9e` (blue)
  - Gardnerella vaginalis: `#e8b723` (yellow)
- Heatmap colormap: `PuOr` (Purple-Orange, range: -1000 to 1000)

---

## Workflow

1. **Generate flux data**: Run gap-split flux sampling on SBML models to produce `.sbml.csv` files
2. **Cluster data**: Run `Clustering.py` to perform PCA/t-SNE/MDS and generate `data_to_plot.csv`
3. **Visualize centroids**: Run `centroidcalculations.py` to create scatter plots with statistical analysis
4. **Create heatmaps**: Run `flux_heatmap.py` to visualize flux patterns across reactions

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn` (PCA, TSNE, MDS, KMeans)
- `scipy` (spatial distance, statistics)
- `mycolorpy` (color palettes)

