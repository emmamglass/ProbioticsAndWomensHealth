# Fig4F: D-lactic Acid vs Growth AUC

This folder is named for its manuscript panel target: `Fig4F` corresponds to Figure 4, panel F.

This folder contains the script used to model the relationship between growth AUC and D-lactic acid concentration.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `dlacticandgrowth.py`
- Uses hard-coded paired `x`/`y` values for AUC and D-lactic acid
- Fits an exponential curve (`y = a * exp(bx)`)
- Computes and prints `R^2`
- Plots colored points and fitted curve

## Required Input Files

- None (all numeric data is embedded directly in `dlacticandgrowth.py`)

## Dependencies

- `numpy`
- `scipy`
- `scikit-learn`
- `matplotlib`
