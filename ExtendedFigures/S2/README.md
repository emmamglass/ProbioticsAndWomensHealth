# S2: Inhibitory/Uninhibitory Flux Heatmap

This folder is named for its supplemental/extended-data target: `S2` corresponds to Supplemental Figure S2.

This folder contains a script that builds a clustered heatmap of **median metabolic flux values** for multiple vaginal commensal groups plus *Gardnerella vaginalis*.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Script

### `flux_heatmap_inhib_uninhib.py`
The script:
- Reads 4 text files listing flux CSV filenames.
- For each listed flux CSV, computes the **median** flux per reaction (median across rows).
- Filters reactions by:
  - low variance (variance < `0.1`)
  - high correlation (drops columns correlated > `0.9`)
- Renames species rows using `file_species_mapping.csv`.
- Colors columns by metabolic subsystem using `all_reactions.csv`.
- Produces a seaborn clustered heatmap (`sns.clustermap`) and displays it.

## Input Files Required

### A) Flux CSV filename lists (one flux CSV per line)
- `uninhibitory_vag_comm.txt`
- `moderate_vag_comm.txt`
- `inhibitory_vag_comm.txt`
- `gardnerella_vaginalis.txt`

Each `.txt` file should contain the flux CSV filenames/paths (one per line) that the script will load with `pd.read_csv(fn)`.

### B) Mapping tables (in the same folder as the script)
- `file_species_mapping.csv`
  - Expected columns: `file_name`, `species`
- `all_reactions.csv`
  - Expected columns: `reaction`, `subsystem`

## Flux CSV location note (important)

The script calls `pd.read_csv(fn)` using the strings read from the `.txt` list files.

If your flux CSVs are stored in an external folder such as `../FluxSamplingFiles/HumanAssociated/`, then each entry in the `.txt` files must be resolvable as:
- a relative path from `S2/`, or
- an absolute path.

## Output

- A clustered heatmap displayed via `plt.show()`.
- Writes `all_reactions.txt` into the `S2/` folder (reaction list before filtering).

## Dependencies

- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
