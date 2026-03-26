# Probiotics and Women's Health

This repository contains figure-organized computational and experimental analyses for studying metabolic interactions among probiotics, commensals, and pathogens in the context of women's health (with a strong focus on vaginal ecology and *Gardnerella vaginalis* inhibition phenotypes).

## What Is In This Repository

- **Figure-organized analysis code** under `Figures/` (main manuscript figures).
- **Supplemental/extended figure code and data** under `ExtendedFigures/`.
- **Pairwise community modeling workflow for Table 6** under `Table6_MICOM/`.
- **Genome-scale metabolic network model resources (GENREs)** under `GENREs/`.
- **Flux sampling data pool** under `FluxSamplingFiles/`, referenced by multiple figure scripts.

## Folder Naming Convention

Folder names are intentional and map to manuscript artifacts:

- `Figures/FigX/...` -> Figure X in the manuscript.
- `Figures/FigX/FigXY` -> panel-level folder (for example `Fig3A`, `Fig4F`).
- `ExtendedFigures/SY` -> supplemental/extended figure SY.
- `Table6_MICOM` -> analyses supporting Table 6.
- `GENREs/...` -> shared model resources reused across multiple analyses.

Use folder names as the primary index for which scripts and data correspond to each manuscript item.

## Top-Level Layout

```text
ProbioticsAndWomensHealth/
├── Figures/
│   ├── Fig1/
│   ├── Fig2/
│   ├── Fig3/
│   └── Fig4/
├── ExtendedFigures/
│   ├── S1/
│   ├── S2/
│   ├── S3/
│   ├── S4/
│   └── S5/
├── Table6_MICOM/
├── GENREs/
├── FluxSamplingFiles/
├── PSEUDOCODE.txt
└── README.md
```

---

## Main Figure Pipelines

### Figure 1 (`Figures/Fig1`)

**Script**
- `probioticsanalysis.py`

**Primary input**
- `BinarySpeciesPresence.csv`

**What it produces**
- Brand-level boxplot of number of species.
- Histogram of species counts across products.
- PCA scatter visualization from binary species-presence matrix.

---

### Figure 2 (`Figures/Fig2`)

#### Fig2B (`Figures/Fig2/Fig2B`)
- `ReactionAnalysisUpsetPlot.py`
- `ReactionAnnotation.py`
- Focus: reaction overlap and annotation workflows.

#### Fig2C (`Figures/Fig2/Fig2C`)
- `ReactionAnnotation.py`
- `subsystem_differences_hist.py`
- Focus: subsystem differences for pairwise group comparisons.

#### Fig2DEF (`Figures/Fig2/Fig2DEF`)
- `ReactionAnnotation.py`
- `Unique_subystem_comparison.py`
- Focus: unique reaction subsystem enrichment-style summaries.

#### Fig2G (`Figures/Fig2/Fig2G`)
- `Clustering.py`
- `centroidcalculations.py`
- Focus: probiotic-focused clustering and centroid statistics.

#### Fig2H (`Figures/Fig2/Fig2H`)
- `Clustering.py`
- `centroidcalculations.py`
- `flux_heatmap.py`
- Focus: commensal/pathogen/probiotic clustering + reaction heatmap.

---

### Figure 3 (`Figures/Fig3`)

#### Fig3A (`Figures/Fig3/Fig3A`)

**Scripts**
- `clusteringvaginalproandcomm.py`
- `centroidcalculations_vagina.py`

**Role split**
- `clusteringvaginalproandcomm.py` generates reduced coordinates and writes `data_to_plot_vagina.csv`.
- `centroidcalculations_vagina.py` performs centroid/ellipse statistics and plotting.

#### Fig3B (`Figures/Fig3/Fig3B`)

**Script**
- `flux_heatmap_inhib_uninhib.py`

**Heatmap grouping**
- Uninhibitory vaginal commensals
- Moderate vaginal commensals
- Inhibitory vaginal commensals
- *Gardnerella vaginalis*

**Important input-path note**
- Flux CSVs are loaded from file paths listed in group `.txt` files.
- If flux files live outside the figure folder (for example in `FluxSamplingFiles/HumanAssociated/`), list entries must be valid relative/absolute paths from the runtime working directory.

---

### Figure 4 (`Figures/Fig4`)

#### Fig4A (`Figures/Fig4/Fig4A`)
- `plot_curves.py`
- Input: `Final.csv`
- Output: growth curves with mean and SEM shading.

#### Fig4B (`Figures/Fig4/Fig4B `)
- `AUC_difference.py`
- Input: `Final.csv`
- Output: AUC-based bar comparison with ANOVA/pairwise tests and `species_auc_values.csv`.
- Note: folder currently includes a trailing space (`Fig4B `).

#### Fig4C (`Figures/Fig4/Fig4C`)
- `pHplot.py`
- Input: data embedded directly in script (no spreadsheet required).

#### Fig4D (`Figures/Fig4/Fig4D`)
- `Llactic.py`
- Input: data embedded directly in script (no spreadsheet required).

#### Fig4E (`Figures/Fig4/Fig4E`)
- `dlactic.py`
- Input: data embedded directly in script (no spreadsheet required).

#### Fig4F (`Figures/Fig4/Fig4F`)
- `dlacticandgrowth.py`
- Input: data embedded directly in script (no spreadsheet required).
- Output: exponential fit and reported `R^2`.

---

## Supplemental / Extended Figure Pipelines

### S1 (`ExtendedFigures/S1`)
- `PubMed_published_articles.py`
- Input: `PubMed_Probiotics_Timeline_Results_by_Year.csv`
- Output: publication timeline plot.

### S2 (`ExtendedFigures/S2`)
- `flux_heatmap_inhib_uninhib.py`
- Inputs:
  - `uninhibitory_vag_comm.txt`
  - `moderate_vag_comm.txt`
  - `inhibitory_vag_comm.txt`
  - `gardnerella_vaginalis.txt`
  - `file_species_mapping.csv`
  - `all_reactions.csv`
  - flux CSVs referenced by those list files
- Output:
  - heatmap visualization
  - `all_reactions.txt` (generated)

### S4 (`ExtendedFigures/S4`)
- `plot_curves.py`
- Inputs:
  - `Final.csv`
  - `PGY_mcur_final.csv`
- Output: combined growth-curve plot.

`S3` and `S5` hold additional supplemental data/materials (for example data files used for supplement support) and can be treated as supplemental data containers unless a script is present.

---

## Table Workflow

### Table 6 (`Table6_MICOM`)

**Main scripts**
- `pairwise_community_modeling.py`
- `create_plots_from_csv.py`

**Purpose**
- Pairwise metabolic community modeling to compare inhibition behavior and mechanistic metrics (growth suppression, niche overlap, metabolite-related behavior) across candidate strain pairs.

**Typical artifacts**
- summary CSV outputs
- serialized intermediate results
- manuscript-style plots

**Environment notes**
- This folder includes local virtual environments (`venv`, `venv311`) and run logs for reproducibility.

---

## Shared Model Resources

### `GENREs/`

Contains curated genome-scale models and associated underlying data resources used across figure and table analyses:

- `GENREs/GENREs/HumanAssociatedMetabolicNetworkModels`
- `GENREs/GENREs/PathogenicMetabolicNetworkModels`
- `GENREs/GENREs/ProbioticMetabolicNetworkModels`
- `GENREs/DataUnderlyingGENREs` (resource/supporting data)

These are shared assets, not single-figure folders.

---

## Data Types Used

- **SBML (`.sbml`)**: genome-scale model files.
- **Flux CSVs (`.sbml.csv`)**: sampled flux distributions from models.
- **List files (`.txt`)**: pointers to flux CSVs grouped by phenotype/class.
- **Result CSVs**: transformed coordinates, summary statistics, and table data.

---

## Python Dependencies (Repository-Wide)

The scripts across this repository use combinations of:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy`
- `scikit-learn`
- `cobra`
- `micom` (Table 6 workflows)
- `upsetplot` (reaction overlap plotting)
- `mycolorpy`
- `requests`
- `biopython` (`Bio` imports in annotation scripts)
- `colour`

Not every folder needs every package; see folder-level README files for precise local requirements.

---

## How To Navigate and Run

1. Start from manuscript target:
   - choose folder by artifact name (`Fig3A`, `S2`, `Table6_MICOM`, etc.).
2. Open that folder’s `README.md`:
   - confirm script order, inputs, and expected outputs.
3. Verify list-file paths:
   - especially for flux heatmaps/clustering scripts that load CSVs from `.txt` path lists.
4. Run scripts from the folder they expect:
   - many scripts use relative paths and assume local working directory context.

---

## Notes on Current State

- Folder and script organization has been normalized around figure/table/supplement naming.
- Some historical naming artifacts remain (for example `Figures/Fig4/Fig4B ` with trailing space).
- `PSEUDOCODE.txt` provides a workflow-level, script-by-script pseudocode summary aligned to this structure.

---

## License

MIT License.

