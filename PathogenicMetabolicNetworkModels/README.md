# Pathogenic Metabolic Network Models

This folder contains genome-scale metabolic network models (GEMs) for pathogenic bacteria in SBML format.

## Contents

- **197 SBML model files** (`.sbml` format)
- Each file represents a genome-scale metabolic model for a pathogenic bacterial species

## Model Format

- **SBML** (Systems Biology Markup Language) version 3.1 or compatible
- Models are constraint-based and suitable for:
  - Flux Balance Analysis (FBA)
  - Flux sampling (e.g., using gap-split or ACHR)
  - Metabolic network analysis

## Usage

These models are used in conjunction with:
- Flux sampling scripts (to generate `.sbml.csv` flux files)
- Clustering analyses (`CommensalPathogenProbioticClustering/`)
- Reaction analysis (`ReactionAnalysis/`)

## Inputs / Outputs for Scripts

- **Inputs**: `.sbml` model files are consumed by downstream sampling/clustering scripts; no additional CSV input is required within this folder.
- **Outputs**: This folder itself produces no output; downstream scripts write flux CSVs, plots, and tables in their respective directories.

## Model Sources

Models are likely derived from:
- ModelSEED database
- CarveMe reconstructions
- Manual curation
- Other automated reconstruction pipelines

## Related Scripts

See:
- `CommensalPathogenProbioticClustering/` - For clustering analysis using flux data from these models
- `ReactionAnalysis/` - For analyzing reactions and subsystems in these models

