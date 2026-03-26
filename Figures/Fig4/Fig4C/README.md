# Fig4C: Media pH by Group

This folder is named for its manuscript panel target: `Fig4C` corresponds to Figure 4, panel C.

This folder contains the script used to compare media pH across uninhibitory, moderate, and inhibitory groups.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `pHplot.py`
- Computes group means and SEMs
- Performs pairwise Welch's t-tests
- Plots bar chart with significance annotations

## Input Data Note

- The pH values are defined directly inside `pHplot.py` as Python lists.
- No spreadsheet or CSV input file is required for this figure.

## Required Input Files

- None (data is embedded in script)

## Dependencies

- `numpy`
- `scipy`
- `matplotlib`
