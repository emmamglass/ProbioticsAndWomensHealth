# Commensal Metabolic Network Models

This folder contains genome-scale metabolic network models (GEMs) for commensal bacteria in SBML format.

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


