# Spent Media Experiment Analysis

This folder contains scripts and data for analyzing experimental growth assays and metabolite measurements from spent media experiments.

## Overview

Spent media experiments test how *Gardnerella vaginalis* grows in spent media (conditioned media) from various vaginal commensal and probiotic species. This helps identify which species produce metabolites that inhibit or promote pathogen growth.

## Folder Structure

```
SpentMediaExperiment/
├── GV14018/              # Experiments with Gardnerella vaginalis strain 14018
├── JCP7672/              # Experiments with Gardnerella vaginalis strain JCP7672
├── LacticAcid/           # Lactic acid concentration measurements
│   ├── DLacticAcid/      # D-lactic acid analysis
│   └── LLacticAcid/      # L-lactic acid analysis
└── pH/                   # pH measurements
```

## Subfolders

### GV14018/
Experiments using *Gardnerella vaginalis* strain 14018.

#### Files:
- **`plot_curves.py`**: Plots growth curves with standard error bars
- **`AUC_difference.py`**: Calculates Area Under the Curve (AUC) and performs statistical comparisons
- **`Final.csv`**: Growth curve data (OD 600 vs. time)
- **`PGY_mcur_final.csv`**: Additional growth curve data
- **`*.csv`**: Individual condition data files

#### `plot_curves.py`
**Purpose**: Visualizes growth curves from spent media experiments.

**Functionality**:
- Loads growth data from `Final.csv` and optionally `PGY_mcur_final.csv`
- Extracts time (Duration/Hours) and OD 600 measurements
- Groups replicates by condition (removes replicate numbers)
- Calculates mean and standard error across replicates
- Plots growth curves with:
  - Mean line for each condition
  - Shaded error bands (mean ± SEM)
  - Custom color scheme for each species

**Usage**:
```bash
python plot_curves.py
```

**Input Files Required**:
- `Final.csv` - Columns: Duration (Hours), [Condition] [Replicate]
- `PGY_mcur_final.csv` (optional) - Additional data

**Output**:
- Growth curve plot showing all conditions
- Legend with species names

**Color Scheme**: Custom colors for each species (see script for full list)

---

#### `AUC_difference.py`
**Purpose**: Calculates Area Under the Curve (AUC) and compares groups statistically.

**Functionality**:
- Loads growth data from `Final.csv`
- Normalizes data (subtracts global minimum)
- Groups species into:
  - **Uninhibitory**: Species that don't inhibit growth
  - **Moderate**: Species with moderate inhibitory effect
  - **Inhibitory**: Species that strongly inhibit growth
- Calculates AUC for each replicate using Simpson's integration
- Computes mean and standard deviation AUC per species
- Performs statistical tests:
  - **One-way ANOVA** for overall group differences
  - **Pairwise t-tests** between groups
- Creates bar chart with:
  - Mean AUC per group
  - Error bars (standard deviation)
  - Significance indicators

**Usage**:
```bash
python AUC_difference.py
```

**Input Files Required**:
- `Final.csv` - Growth curve data

**Output**:
- Bar chart comparing mean AUC by group
- `species_auc_values.csv` - AUC values for each species
- Console output with statistical test results

**Group Definitions**:
- Uninhibitory: PGY (Modified) Media, M. curtisii SM, V. bacterium SM, E. massiliensis SM
- Moderate: P. vaginalis SM, A. marseille SM, C. bergeronii SM, A. christensenii SM
- Inhibitory: F. vaginae SM, A. lactolyticus SM, A. tetradius SM, L. jensenii SM

---

### JCP7672/
Experiments using *Gardnerella vaginalis* strain JCP7672.

#### Files:
- **`plot_curves.py`**: Similar to GV14018 version, plots growth curves
- **`Final.csv`**: Growth curve data
- **`*.csv`**: Individual condition data files

#### `plot_curves.py`
**Purpose**: Visualizes growth curves for JCP7672 strain.

**Functionality**: Similar to GV14018 version, adapted for JCP7672 data structure.

---

### LacticAcid/DLacticAcid/
Analysis of D-lactic acid concentrations in spent media.

#### Files:
- **`dlactic.py`**: Bar chart comparing D-lactic acid by group
- **`dlacticandgrowth.py`**: Correlation analysis between D-lactic acid and growth (AUC)
- **`*.xlsx`**: Excel files with D-lactic acid concentration data

#### `dlactic.py`
**Purpose**: Compares D-lactic acid concentrations across inhibitory groups.

**Functionality**:
- Loads D-lactic acid concentration data
- Groups data into Uninhibitory, Moderate, and Inhibitory
- Calculates means and standard errors
- Performs pairwise Welch's t-tests (one-sided, greater)
- Creates bar chart with significance indicators

**Usage**:
```bash
python dlactic.py
```

**Output**:
- Bar chart showing D-lactic acid concentration by group
- Statistical test results

**Key Finding**: Inhibitory groups have significantly higher D-lactic acid concentrations.

---

#### `dlacticandgrowth.py`
**Purpose**: Analyzes correlation between D-lactic acid and *G. vaginalis* growth.

**Functionality**:
- Loads D-lactic acid concentrations and AUC values
- Fits exponential model: `y = a * exp(b * x)`
- Calculates R² for model fit
- Creates scatter plot with:
  - Color-coded points by group
  - Fitted exponential curve

**Usage**:
```bash
python dlacticandgrowth.py
```

**Output**:
- Scatter plot with exponential fit
- Model equation and R² value

**Key Finding**: D-lactic acid concentration correlates inversely with growth (higher D-lactic acid = lower growth).

---

### LacticAcid/LLacticAcid/
Analysis of L-lactic acid concentrations in spent media.

#### Files:
- **`Llactic.py`**: Bar chart comparing L-lactic acid by group
- **`*.xlsx`**: Excel files with L-lactic acid concentration data

#### `Llactic.py`
**Purpose**: Compares L-lactic acid concentrations across inhibitory groups.

**Functionality**: Similar to `dlactic.py` but for L-lactic acid.

**Usage**:
```bash
python Llactic.py
```

**Output**:
- Bar chart showing L-lactic acid concentration by group
- Statistical test results

---

### pH/
Analysis of pH measurements in spent media.

#### Files:
- **`pHplot.py`**: Bar chart comparing pH by group

#### `pHplot.py`
**Purpose**: Compares pH values across inhibitory groups.

**Functionality**:
- Loads pH measurement data
- Groups data into Uninhibitory, Moderate, and Inhibitory
- Calculates means and standard errors
- Performs pairwise Welch's t-tests (one-sided, less)
- Creates bar chart with significance indicators

**Usage**:
```bash
python pHplot.py
```

**Output**:
- Bar chart showing pH by group
- Statistical test results

**Key Finding**: Inhibitory groups have significantly lower pH (more acidic).

---

## Key Findings

1. **Inhibitory Classification**: Vaginal commensals can be classified as inhibitory, moderate, or uninhibitory based on their effect on *G. vaginalis* growth.

2. **D-Lactic Acid**: Higher D-lactic acid concentrations correlate with growth inhibition.

3. **pH Effect**: Lower pH (more acidic) is associated with inhibitory phenotypes.

4. **Strain Differences**: Results may vary between *G. vaginalis* strains (14018 vs. JCP7672).

## Workflow

1. **Collect experimental data**: Growth curves, metabolite concentrations, pH measurements
2. **Plot growth curves**: Use `plot_curves.py` to visualize growth
3. **Calculate AUC**: Use `AUC_difference.py` to quantify growth and compare groups
4. **Analyze metabolites**: Use lactic acid and pH scripts to identify mechanisms
5. **Correlate**: Use `dlacticandgrowth.py` to link metabolites to growth inhibition

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy` (statistical tests, numerical integration)
- `scikit-learn` (for R² calculation in correlation analysis)

