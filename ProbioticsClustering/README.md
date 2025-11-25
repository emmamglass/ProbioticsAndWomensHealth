# Probiotics Clustering Analysis

This folder contains scripts for clustering and analyzing metabolic flux data specifically from probiotic bacteria.

## Files

### `Clustering.py`
**Purpose**: Performs dimensionality reduction on flux data from probiotic species, grouped by family.

**Functionality**:
- Reads flux data from `.sbml.csv` files (output from gap-split flux sampling)
- Classifies species as Probiotic based on `probiotics_flux_list.txt`
- Classifies species as Pathogen based on `pathogens_flux_list.txt`
- All other species are classified as Commensal
- Downsamples flux data (default: 500 samples per species)
- Performs dimensionality reduction using:
  - **PCA** (Principal Component Analysis) - default
  - **t-SNE** (t-distributed Stochastic Neighbor Embedding)
  - **MDS** (Multidimensional Scaling with Bray-Curtis distance)
  - **K-means** (for elbow method to determine optimal cluster number)
- Outputs variance explained by principal components (for PCA)

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

**Note**: This script is similar to `CommensalPathogenProbioticClustering/Clustering.py` but focuses specifically on probiotic analysis.

---

### `centroidcalculations.py`
**Purpose**: Calculates and visualizes centroids for probiotic species grouped by family.

**Functionality**:
- Loads clustered data from `data_to_plot.csv`
- Groups probiotic species by family:
  - Lactobacillaceae
  - Streptococcaceae
  - Bacillaceae
  - Bifidobacteriaceae
  - Akkermansiaceae
  - Enterococcaceae
- Computes centroids for each family
- Calculates distances from centroids
- Draws confidence ellipses (2 standard deviations) around centroids
- Performs Kruskal-Wallis test to assess significance of family-level clustering
- Creates scatter plot with color-coded families and centroid markers

**Usage**:
```bash
python centroidcalculations.py
```

**Input Files Required**:
- `data_to_plot.csv` - Output from `Clustering.py` containing:
  - Component 1, Component 2 (PCA/t-SNE/MDS coordinates)
  - Classification (family names)

**Output**:
- Scatter plot with:
  - Color-coded points by family (using Spectral color palette)
  - Centroid markers (triangles)
  - Confidence ellipses (2 SD)
- Statistical output:
  - Centroid coordinates
  - Standard deviations
  - Kruskal-Wallis test results

**Color Scheme**: Uses Seaborn's "Spectral" palette for family differentiation.

---

## Workflow

1. **Generate flux data**: Run gap-split flux sampling on probiotic SBML models to produce `.sbml.csv` files
2. **Cluster data**: Run `Clustering.py` to perform PCA/t-SNE/MDS and generate `data_to_plot.csv`
3. **Visualize centroids**: Run `centroidcalculations.py` to create scatter plots grouped by family

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn` (PCA, TSNE, MDS, KMeans)
- `scipy` (spatial distance, statistics)
- `mycolorpy` (color palettes)

