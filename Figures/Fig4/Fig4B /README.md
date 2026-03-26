# Fig4B: AUC Group Comparison

This folder is named for its manuscript panel target: `Fig4B` corresponds to Figure 4, panel B.

This folder contains the script used to compare normalized AUC values across uninhibitory, moderate, and inhibitory groups.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `AUC_difference.py`
- Loads and normalizes data from `Final.csv`
- Computes per-species AUC values from replicate growth curves
- Performs one-way ANOVA and pairwise t-tests
- Plots grouped bar chart with significance annotations
- Writes `species_auc_values.csv`

## Required Input Files

- `Final.csv` (required by script)

## Optional/Generated Output

- `species_auc_values.csv` (generated when script runs)

## Other Files in Folder

These CSVs are present in the folder but are not read by `AUC_difference.py`:
- `A._chr_SM___F._vag_SM.csv`
- `A._tet___E._mass.csv`
- `C._ber___A.mar.csv`
- `L._jen_SM___A._lac_SM.csv`
- `P._vag_SM___V._bac_SM.csv`

## Dependencies

- `pandas`
- `numpy`
- `scipy`
- `matplotlib`
