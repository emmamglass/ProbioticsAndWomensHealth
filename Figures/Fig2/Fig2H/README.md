# Commensal-Pathogen-Probiotic Clustering Analysis

This folder is named for its manuscript panel target: `Fig2H` corresponds to Figure 2, panel H.

This folder contains scripts for clustering and visualizing metabolic flux data from commensal, pathogenic, and probiotic bacteria.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

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
- `*.sbml.csv` - Flux sampling output files; each file should contain one row per sampled flux vector and one column per reaction (header row of reaction IDs).
- `probiotics_flux_list.txt` - One probiotic flux CSV filename per line (no header).
- `pathogens_flux_list.txt` - One pathogen flux CSV filename per line (no header).

**Output**:
- Transformed flux data with component coordinates (saved to `data_to_plot.csv` if enabled) with columns: `Component1`, `Component2` (or t-SNE/MDS equivalents), `Label` (filename), `Classification` (Probiotic/Pathogen/Commensal).
- Classification labels and variance explained statistics (for PCA).

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
- `data_to_plot.csv` - Output from `Clustering.py` containing columns `Component1`, `Component2`, `Label`, and `Classification` (Commensal/Pathogen/Probiotic).

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
- `vaginal_probiotic.txt`, `uninhibitory_vag_comm.txt`, `inhibitory_vag_comm.txt`, `gardnerella_vaginalis.txt`: each with one flux CSV filename per line.
- `file_species_mapping.csv`: columns `filename`, `species`.
- `all_reactions.csv`: columns `reaction_id`, `subsystem`.
- Flux CSV files referenced above (`*.sbml.csv`), structured as rows = samples, columns = reaction IDs (header row).

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

---

## Input File Location Notes (Current Setup)

The scripts in this folder read flux CSVs using relative paths from the current working directory:

- `Clustering.py` searches for `*.sbml.csv` in the current directory.
- `flux_heatmap.py` reads CSV paths listed in:
  - `vaginal_probiotic.txt`
  - `uninhibitory_vag_comm.txt`
  - `inhibitory_vag_comm.txt`
  - `gardnerella_vaginalis.txt`

If your flux CSV files are stored in `../FluxSamplingFiles/HumanAssociated/`, then either:

1. run scripts from a directory where listed paths resolve correctly, or
2. update list files to include relative paths like `../FluxSamplingFiles/HumanAssociated/<file>.sbml.csv`, and
3. for `Clustering.py`, copy/symlink CSVs locally or update the script to glob `../FluxSamplingFiles/HumanAssociated/*.sbml.csv`.

## File Check Results (Mar 25, 2026)

Present in this folder:

- `Clustering.py`, `centroidcalculations.py`, `flux_heatmap.py`
- `probiotics_flux_list.txt`, `pathogens_flux_list.txt`
- `vaginal_probiotic.txt`, `uninhibitory_vag_comm.txt`, `inhibitory_vag_comm.txt`, `gardnerella_vaginalis.txt`
- `file_species_mapping.csv`, `all_reactions.csv`, `data_to_plot.csv`

Flux CSV availability check against `../FluxSamplingFiles/HumanAssociated/`:

- `probiotics_flux_list.txt`: 33/35 not found in `HumanAssociated` (10 not found anywhere under `../FluxSamplingFiles/`)
- `pathogens_flux_list.txt`: 198/198 not found in `HumanAssociated` (0 missing globally under `../FluxSamplingFiles/`)
- `vaginal_probiotic.txt`: 20/20 not found in `HumanAssociated` (6 not found globally)
- `uninhibitory_vag_comm.txt`: 0/3 missing in `HumanAssociated`
- `inhibitory_vag_comm.txt`: 0/4 missing in `HumanAssociated`
- `gardnerella_vaginalis.txt`: 2/2 missing in `HumanAssociated` (2 not found globally)

Missing globally under `../FluxSamplingFiles/` (detected from list files):

- `probiotics_flux_list.txt`: `239935.2189.sbml.csv`, `1613.511.sbml.csv`, `1598.864.sbml.csv`, `79880.20.sbml.csv`, `1682.258.sbml.csv`, `47715.1833.sbml.csv`, `278197.12.sbml.csv`, `33959.508.sbml.csv`, `47770.632.sbml.csv`, `1308.1128.sbml.csv`
- `vaginal_probiotic.txt`: `1682.258.sbml.csv`, `1613.511.sbml.csv`, `1598.864.sbml.csv`, `47770.632.sbml.csv`, `47715.1833.sbml.csv` (plus one duplicate `1682.258.sbml.csv` entry)
- `gardnerella_vaginalis.txt`: `585528.19.sbml.csv`, `1261060.4.sbml.csv`

