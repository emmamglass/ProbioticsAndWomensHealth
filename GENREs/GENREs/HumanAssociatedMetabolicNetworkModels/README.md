# Commensal Metabolic Network Models

Folder naming context: this is a shared model-resource folder (`HumanAssociatedMetabolicNetworkModels`) used across multiple figure/table analyses, rather than a single figure-specific output folder.

This folder contains genome-scale metabolic network models (GEMs) for commensal bacteria in SBML format.

## Standard README Template

- **Folder-to-manuscript mapping**: Shared resource folder used across multiple figures/tables.
- **Common section structure**: `Purpose`, `Scripts/Contents`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Contents

- **775 SBML model files** (`.sbml` format)
- Each file represents a genome-scale metabolic model for a commensal bacterial species

## Model Format

- **SBML** (Systems Biology Markup Language) version 3.1 or compatible
- Models are constraint-based and suitable for:
  - Flux Balance Analysis (FBA)
  - Flux sampling (e.g., using gap-split)
  - Metabolic network analysis

## Usage

These models are used in conjunction with:
- Flux sampling scripts (to generate `.sbml.csv` flux files)
- Clustering analyses (`CommensalPathogenProbioticClustering/`)
- Reaction analysis (`ReactionAnalysis/`)

## Inputs / Outputs for Scripts

- **Inputs**: `.sbml` model files here are read by downstream sampling/clustering/analysis scripts; no CSV inputs are required within this folder.
- **Outputs**: This folder produces no outputs itself; downstream scripts generate flux CSVs, plots, and tables elsewhere.

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


