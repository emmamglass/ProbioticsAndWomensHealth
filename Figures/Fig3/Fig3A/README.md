# Fig3A: Vaginal Probiotic vs Commensal Clustering

This folder is named for its manuscript panel target: `Fig3A` corresponds to Figure 3, panel A.

This folder contains the scripts used to generate the Fig3A clustering and centroid analyses.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Files

### `clusteringvaginalproandcomm.py`
**Purpose**: Perform dimensionality reduction on vaginal probiotic and vaginal commensal flux samples.

**Functionality**:
- Reads flux data from `.sbml.csv` files.
- Assigns class labels from:
  - `vaginal_probiotic.txt` -> `Vaginal Probiotic`
  - `vagina_commensals_flux_list.txt` -> `Vaginal Commensal`
- Skips files not listed in either text file.
- Supports `pca`, `tsne`, `mds`, and `kmeans` modes.
- In the current script entrypoint, runs PCA with `downsample=250`.
- Writes transformed coordinates to `data_to_plot_vagina.csv`.

**Input files required**:
- Flux CSV files (`*.sbml.csv`) for listed species.
- `vaginal_probiotic.txt`
- `vagina_commensals_flux_list.txt`

**Important path note**:
- The script currently uses `glob.glob('*.sbml.csv')`, so it only discovers CSVs in the current working directory.
- If flux files are stored outside this folder (for example in `../FluxSamplingFiles/HumanAssociated/`), update the glob path or run from a directory where the paths resolve correctly.

**Output**:
- `data_to_plot_vagina.csv` with columns:
  - `Component 1`
  - `Component 2`
  - `Label`
  - `Classification`

---

### `centroidcalculations_vagina.py`
**Purpose**: Compute centroids and confidence ellipses for the Fig3A classes.

**Functionality**:
- Loads `data_to_plot_vagina.csv`.
- Computes centroids for `Vaginal Commensal` and `Vaginal Probiotic`.
- Computes within-class distances and covariance.
- Plots scatter + centroid markers + confidence ellipses.
- Runs Kruskal-Wallis test on class distance distributions.

**Input files required**:
- `data_to_plot_vagina.csv` (from `clusteringvaginalproandcomm.py`)

## Workflow

1. Run `clusteringvaginalproandcomm.py` to generate `data_to_plot_vagina.csv`.
2. Run `centroidcalculations_vagina.py` to generate the Fig3A visualization/statistics.

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `scipy`
- `mycolorpy`
