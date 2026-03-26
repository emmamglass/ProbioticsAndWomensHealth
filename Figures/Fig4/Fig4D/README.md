# Fig4D: L-lactic Acid by Group

This folder is named for its manuscript panel target: `Fig4D` corresponds to Figure 4, panel D.

This folder contains the script used to compare L-lactic acid concentration across uninhibitory, moderate, and inhibitory groups.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `Llactic.py`
- Computes group means and SEMs
- Performs pairwise Welch's t-tests
- Plots bar chart with significance annotations

## Required Input Files

- None (L-lactic acid values are embedded directly in `Llactic.py`)

## Dependencies

- `numpy`
- `scipy`
- `matplotlib`
