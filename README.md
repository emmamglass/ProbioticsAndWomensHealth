# Probiotics and Women's Health

This repository contains computational and experimental analyses investigating the metabolic interactions between probiotics, commensals, and pathogens in the context of women's health, with a particular focus on vaginal microbiota and bacterial vaginosis (BV).

## Repository Overview

This project integrates:
- **Genome-scale metabolic network models** (GEMs) for commensal, pathogenic, and probiotic bacteria
- **Flux balance analysis** (FBA) and flux sampling to characterize metabolic phenotypes
- **Clustering and dimensionality reduction** analyses to identify metabolic patterns
- **Reaction pathway analysis** to understand metabolic differences between bacterial groups
- **Experimental validation** using spent media growth assays and metabolite measurements
- **Meta-analysis** of clinical BV recurrence data

## Repository Structure

```
ProbioticsAndWomensHealth/
├── CommensalMetabolicNetworkModels/     # SBML models for commensal bacteria
├── CommensalPathogenProbioticClustering/ # Clustering analysis comparing all three groups
├── MetaAnalysis/                        # Meta-analysis of clinical BV recurrence data
├── PathogenicMetabolicNetworkModels/    # SBML models for pathogenic bacteria
├── ProbioticMetabolicNetworkModels/     # SBML models for probiotic bacteria
├── ProbioticsClustering/                # Clustering analysis of probiotic species
├── ReactionAnalysis/                    # Reaction pathway and subsystem analysis
├── SpentMediaExperiment/                # Experimental growth and metabolite data
└── VaginalSpeciesClustering/            # Clustering analysis of vaginal species
```

## Key Research Questions

1. **Metabolic Differentiation**: How do metabolic networks differ between commensals, pathogens, and probiotics?
2. **Vaginal Microbiota**: What metabolic features distinguish inhibitory vs. non-inhibitory vaginal commensals?
3. **Mechanisms of Inhibition**: What metabolites or metabolic pathways contribute to growth inhibition of pathogens like *Gardnerella vaginalis*?
4. **Clinical Relevance**: How do probiotic interventions affect BV recurrence rates?

## Main Components

### 1. Metabolic Network Models

The repository contains genome-scale metabolic models (SBML format) for:
- **Commensal bacteria** (775 models)
- **Pathogenic bacteria** (197 models)
- **Probiotic bacteria** (33 models)

These models are used for flux balance analysis and flux sampling to characterize metabolic phenotypes.

### 2. Clustering Analyses

Multiple clustering approaches are used to identify metabolic patterns:
- **PCA** (Principal Component Analysis)
- **t-SNE** (t-distributed Stochastic Neighbor Embedding)
- **MDS** (Multidimensional Scaling)
- **K-means** clustering

See individual folder READMEs for details on each analysis.

### 3. Reaction Analysis

Analysis of metabolic reactions and subsystems to identify:
- Unique reactions in each bacterial group
- Shared vs. unique metabolic pathways
- Subsystem-level differences

### 4. Experimental Validation

Spent media experiments examining:
- Growth curves of *Gardnerella vaginalis* in spent media from various species
- pH measurements
- D- and L-lactic acid concentrations
- Area under the curve (AUC) calculations

### 5. Meta-Analysis

Statistical analysis of clinical BV recurrence data comparing different intervention strategies.

## Dependencies

### Python Packages
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `matplotlib` - Plotting
- `seaborn` - Statistical visualization
- `scikit-learn` - Machine learning (PCA, t-SNE, K-means, MDS)
- `scipy` - Statistical tests and numerical integration
- `cobra` - Constraint-based reconstruction and analysis (COBRA) toolbox
- `upsetplot` - UpSet plots for set intersections
- `mycolorpy` - Color palette generation

### Data Formats
- **SBML** - Systems Biology Markup Language for metabolic models
- **CSV** - Comma-separated values for flux data and experimental results
- **Excel** - Spreadsheet files for experimental data

## System Requirements

- **Operating systems tested**: macOS (Apple silicon) on Darwin 25.1 with Homebrew-managed Python 3.11.14 and 3.14.0 virtual environments. Linux should work with equivalent Python/solver setups; Windows has not been validated.
- **Software dependencies**: Python 3.11+ (3.14 OK), with `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `cobra`, `micom`, `upsetplot`, `mycolorpy`. See `CommunityModeling/requirements.txt` for pinned versions used in MICOM workflows.
- **Solvers**: MICOM uses COBRA solvers; GLPK works out of the box. Gurobi (optional) improves performance if licensed.
- **Hardware**: No non-standard hardware required. A typical desktop/laptop with ≥4 CPU cores and ≥16 GB RAM is recommended for running multiple community simulations. GPU is not used.

## Installation

Typical install on a normal desktop computer (Python already installed):

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r CommunityModeling/requirements.txt
# optional: add plotting/analysis extras
pip install scikit-learn scipy upsetplot mycolorpy
```

If using Gurobi, install and license it separately, then set `MICOM_SOLVER=gurobi`.

## Demo

Run the pairwise community modeling example included in `CommunityModeling`:

```bash
cd /Users/eglass/Desktop/UVA/Nautre\ Microbiology/ProbioticsAndWomensHealth
source .venv/bin/activate      # if created as above
python CommunityModeling/pairwise_community_modeling.py
```

**Expected output** (written to `CommunityModeling/pairwise_results/`):
- `pairwise_summary.csv`, `detailed_results.pkl`
- Plots: `pairwise_comparison_plots.png`, `abundance_dependent_effects.png`

**Expected run time**: ~3–6 minutes on a recent Apple silicon or comparable CPU desktop with 16 GB RAM using the default GLPK solver (Gurobi can be faster).

For all other analyses and scripts, see the README in each subfolder (e.g., `CommensalPathogenProbioticClustering/README.md`, `ProbioticsClustering/README.md`, `ReactionAnalysis/README.md`, etc.) for dataset requirements, parameters, and run commands specific to that module.

## Instructions for Use

- **Prepare models**: Place your SBML models in the relevant module directory (e.g., `CommunityModeling/`) and update the `MODEL_MAPPINGS` dictionary in `pairwise_community_modeling.py` to point to your filenames.
- **Media and constraints**: Adjust media composition in `define_media_constraints()` inside the same script to match your experimental conditions (e.g., PGY-mod or Synthetic Vaginal Fluid).
- **Solver selection**: Set `MICOM_SOLVER` to `glpk` (default), `glpk_exact`, `hybrid`, `osqp`, `scipy`, or `gurobi` if installed.
- **Run on your data**: Execute the script as in the Demo section; outputs will be written to `pairwise_results/` with metrics on growth suppression, niche overlap, and metabolite production.
- **Post-processing**: Use the generated CSV/Pickle outputs to make additional plots or statistical comparisons; see subfolder READMEs for analysis-specific guidance.

## Usage

Each subfolder contains specific analyses. See the README files in each folder for:
- Required input files
- Script execution instructions
- Output descriptions
- Dependencies

## Citation

If you use this repository, please cite the associated publication (if available) or acknowledge the authors.

## Contact

For questions or issues, please contact the repository maintainers.

## License

This repository is licensed under the MIT License. See the license text below:

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

