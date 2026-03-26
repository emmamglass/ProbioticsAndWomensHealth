# S1: PubMed Timeline Plot

This folder is named for its supplemental/extended-data target: `S1` corresponds to Supplemental Figure S1.

This folder contains a small script to plot the number of PubMed articles containing the word/probiotics-related keyword over time.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `PubMed_published_articles.py`
- Loads a timeline results CSV into a DataFrame.
- Plots `Year` vs `Count` as a line chart.

## Input Files Required

- `PubMed_Probiotics_Timeline_Results_by_Year.csv`
  - Must include columns:
    - `Year`
    - `Count`

## Output

- A matplotlib plot displayed via `plt.show()` (not automatically saved to disk).

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
