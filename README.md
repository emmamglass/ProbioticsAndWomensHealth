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

