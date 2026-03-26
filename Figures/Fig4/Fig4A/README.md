# Fig4A: Growth Curves

This folder is named for its manuscript panel target: `Fig4A` corresponds to Figure 4, panel A.

This folder contains the script used to plot the growth curves for the GV14018 spent-media experiment.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `plot_curves.py`
- Loads `Final.csv`
- Computes mean and SEM across replicate columns for each condition
- Plots time-series growth curves with shaded SEM bands

## Required Input Files

- `Final.csv` (required by script)

## Other Files in Folder

These CSVs are present in the folder but are not read by `plot_curves.py`:
- `A._chr_SM___F._vag_SM.csv`
- `A._tet___E._mass.csv`
- `C._ber___A.mar.csv`
- `L._jen_SM___A._lac_SM.csv`
- `P._vag_SM___V._bac_SM.csv`

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
