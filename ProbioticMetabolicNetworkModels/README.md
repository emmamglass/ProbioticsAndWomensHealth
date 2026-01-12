# Probiotic Metabolic Network Models

This folder contains genome-scale metabolic network models (GEMs) for probiotic bacteria in SBML format.

## Contents

- **33 SBML model files** (`.sbml` format)
- Each file represents a genome-scale metabolic model for a probiotic bacterial species

## Model Format

- **SBML** (Systems Biology Markup Language) version 3.1 or compatible
- Models are constraint-based and suitable for:
  - Flux Balance Analysis (FBA)
  - Flux sampling (e.g., using gap-split or ACHR)
  - Metabolic network analysis

## Model Files

The folder contains models for various probiotic species, including:
- Lactobacilli (e.g., *Lactobacillus* species)
- Bifidobacteria (e.g., *Bifidobacterium* species)
- Other probiotic genera

## Usage

These models are used in conjunction with:
- Flux sampling scripts (to generate `.sbml.csv` flux files)
- Clustering analyses:
  - `CommensalPathogenProbioticClustering/` - Comparing all three groups
  - `ProbioticsClustering/` - Focused probiotic analysis
- Reaction analysis (`ReactionAnalysis/`)

## Inputs / Outputs for Scripts

- **Inputs**: Each `.sbml` file is consumed by downstream scripts (flux sampling, clustering, reaction analysis). No CSV inputs are required in this folder itself.
- **Outputs**: This folder does not produce outputs on its own; downstream scripts generate flux CSVs or plots in their respective folders after reading these SBML models.

## Model Sources

Models are likely derived from:
- ModelSEED database
- CarveMe reconstructions
- Manual curation
- Other automated reconstruction pipelines

## Related Scripts

See:
- `CommensalPathogenProbioticClustering/` - For clustering analysis comparing probiotics, pathogens, and commensals
- `ProbioticsClustering/` - For detailed probiotic-specific clustering by family
- `ReactionAnalysis/` - For analyzing reactions and subsystems in probiotic models


