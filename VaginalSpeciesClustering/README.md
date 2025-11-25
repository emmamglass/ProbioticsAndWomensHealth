# Vaginal Species Clustering Analysis

This folder contains scripts for clustering and analyzing metabolic flux data from vaginal probiotic and commensal bacteria, with a focus on understanding inhibitory vs. non-inhibitory phenotypes.

## Files

### `clusteringvaginalproandcomm.py`
**Purpose**: Performs dimensionality reduction on flux data from vaginal probiotic and commensal species.

**Functionality**:
- Reads flux data from `.sbml.csv` files (output from gap-split flux sampling)
- Classifies species as:
  - **Vaginal Probiotic** (from `vaginal_probiotic.txt`)
  - **Vaginal Commensal** (from `vagina_commensals_flux_list.txt`)
- Skips species not in either category
- Downsamples flux data (default: 250 samples per species)
- Performs dimensionality reduction using:
  - **PCA** (Principal Component Analysis) - default
  - **t-SNE** (t-distributed Stochastic Neighbor Embedding)
  - **MDS** (Multidimensional Scaling with Bray-Curtis distance)
  - **K-means** (for elbow method to determine optimal cluster number)
- Outputs variance explained by principal components (for PCA)
- Saves transformed data to `data_to_plot_vagina.csv`

**Usage**:
```python
cluster_data = cluster('pca', downsample=250)
```

**Parameters**:
- `clustertype`: 'pca', 'tsne', 'mds', or 'kmeans'
- `downsample`: Number of flux samples per species (default: 500, but script uses 250)

**Input Files Required**:
- `*.sbml.csv` - Flux sampling output files
- `vaginal_probiotic.txt` - List of vaginal probiotic species filenames
- `vagina_commensals_flux_list.txt` - List of vaginal commensal species filenames

**Output**:
- `data_to_plot_vagina.csv` - Transformed flux data with:
  - Component 1, Component 2 (PCA/t-SNE/MDS coordinates)
  - Label (filename)
  - Classification (Vaginal Probiotic/Vaginal Commensal)
- Variance explained statistics (for PCA)

---

### `centroidcalculations_vagina.py`
**Purpose**: Calculates and visualizes centroids for vaginal probiotic vs. commensal species.

**Functionality**:
- Loads clustered data from `data_to_plot_vagina.csv`
- Computes centroids for each classification group (Vaginal Commensal, Vaginal Probiotic)
- Calculates distances from centroids for each data point
- Computes standard deviations and covariance matrices
- Draws confidence ellipses (2 standard deviations) around centroids
- Performs Kruskal-Wallis test to assess significance of clustering
- Creates scatter plot with color-coded groups and centroid markers

**Usage**:
```bash
python centroidcalculations_vagina.py
```

**Input Files Required**:
- `data_to_plot_vagina.csv` - Output from `clusteringvaginalproandcomm.py` containing:
  - Component 1, Component 2 (PCA/t-SNE/MDS coordinates)
  - Classification (Vaginal Commensal/Vaginal Probiotic)

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
- Vaginal Commensal: `#167dcc` (blue)
- Vaginal Probiotic: `#3c7f4d` (green)

---

### `flux_heatmap_inhib_uninhib.py`
**Purpose**: Creates clustered heatmaps of median flux values, grouping vaginal commensals by inhibitory phenotype.

**Functionality**:
- Reads flux data from multiple CSV files
- Groups species into:
  - **Uninhibitory** (vaginal commensals that don't inhibit *G. vaginalis*)
  - **Moderate** (vaginal commensals with moderate inhibitory effect)
  - **Inhibitory** (vaginal commensals that strongly inhibit *G. vaginalis*)
  - **Gardnerella vaginalis** (the pathogen being tested)
- Computes median flux per reaction for each species
- Filters reactions:
  - Removes low-variance reactions (variance < 0.1)
  - Removes highly correlated reactions (correlation > 0.9)
- Maps file names to species names using `file_species_mapping.csv`
- Maps reactions to subsystems using `all_reactions.csv`
- Creates clustered heatmap with:
  - Row colors indicating inhibitory group
  - Column colors indicating metabolic subsystem
  - Hierarchical clustering using Canberra distance and average linkage

**Usage**:
```bash
python flux_heatmap_inhib_uninhib.py
```

**Input Files Required**:
- `uninhibitory_vag_comm.txt` - List of uninhibitory vaginal commensal filenames
- `moderate_vag_comm.txt` - List of moderate inhibitory vaginal commensal filenames
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
  - Uninhibitory: `#66B5E9` (light blue)
  - Moderate: `#3685B9` (medium blue)
  - Inhibitory: `#07568A` (dark blue)
  - Gardnerella vaginalis: `#e8b723` (yellow)
- Heatmap colormap: `PuOr` (Purple-Orange, range: -1000 to 1000)

---

## Workflow

1. **Generate flux data**: Run gap-split flux sampling on vaginal species SBML models to produce `.sbml.csv` files
2. **Cluster data**: Run `clusteringvaginalproandcomm.py` to perform PCA/t-SNE/MDS and generate `data_to_plot_vagina.csv`
3. **Visualize centroids**: Run `centroidcalculations_vagina.py` to create scatter plots comparing vaginal probiotics and commensals
4. **Create inhibitory heatmaps**: Run `flux_heatmap_inhib_uninhib.py` to visualize flux patterns grouped by inhibitory phenotype

## Key Research Question

This analysis addresses: **What metabolic features distinguish inhibitory vaginal commensals from non-inhibitory ones?**

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn` (PCA, TSNE, MDS, KMeans)
- `scipy` (spatial distance, statistics)
- `mycolorpy` (color palettes)

