# Fig3B: Inhibitory-Phenotype Flux Heatmap

This folder is named for its manuscript panel target: `Fig3B` corresponds to Figure 3, panel B.

This folder contains the script and inputs used to generate the Fig3B clustered heatmap.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Files

### `flux_heatmap_inhib_uninhib.py`
**Purpose**: Build a clustered heatmap of median reaction fluxes across vaginal groups.

**Functionality**:
- Loads lists of flux CSV files from:
  - `uninhibitory_vag_comm.txt`
  - `moderate_vag_comm.txt`
  - `inhibitory_vag_comm.txt`
  - `gardnerella_vaginalis.txt`
- Reads each listed flux CSV and computes median flux per reaction.
- Filters reactions:
  - low variance (< 0.1)
  - high correlation (> 0.9)
- Renames row labels using `file_species_mapping.csv`.
- Maps reactions to subsystems using `all_reactions.csv`.
- Generates a clustered heatmap (Canberra distance, average linkage).
- Writes `all_reactions.txt` (reaction list before filtering).

## Input files required

- `uninhibitory_vag_comm.txt`
- `moderate_vag_comm.txt`
- `inhibitory_vag_comm.txt`
- `gardnerella_vaginalis.txt`
- Flux CSV files referenced by those text files
- `file_species_mapping.csv` (columns: `file_name`, `species`)
- `all_reactions.csv` (columns: `reaction`, `subsystem`)

**Important path note**:
- The script reads each filename from the list files and calls `pd.read_csv(fn)`.
- If flux samples are stored outside this folder (for example in `../FluxSamplingFiles/HumanAssociated/`), each entry in the list files must include a resolvable relative or absolute path.

## Output

- Fig3B clustered heatmap visualization
- `all_reactions.txt`

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
