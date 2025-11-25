# Meta-Analysis

This folder contains scripts and data for meta-analysis of clinical bacterial vaginosis (BV) recurrence data.

## Files

### `metaanalysisplot.py`
**Purpose**: Performs statistical analysis and visualization of BV recurrence rates across different intervention categories.

**Functionality**:
- Loads BV recurrence data from `metaanalysisdatatoplot.csv`
- Converts percentage strings to numeric values
- Performs statistical tests:
  - **Kruskal-Wallis test** (non-parametric ANOVA) for overall group differences
  - **Mann-Whitney U tests** for pairwise comparisons
- Creates box plots with:
  - Color-coded boxes for each category
  - Significance bars showing pairwise p-values
  - Significance notation: `***` (p<0.001), `**` (p<0.01), `*` (p<0.05), `ns` (not significant)

**Usage**:
```bash
python metaanalysisplot.py
```

**Input Files Required**:
- `metaanalysisdatatoplot.csv` - CSV file with columns for each intervention category
  - Each column contains percentage values (as strings with '%' suffix)
  - Values represent BV recurrence rates

**Output**:
- Box plot visualization showing:
  - Distribution of BV recurrence rates by category
  - Statistical significance indicators
- Console output:
  - Kruskal-Wallis H-statistic and p-value
  - Pairwise Mann-Whitney U test p-values

**Color Scheme**:
- Uses custom colors: `['#79a6e0', '#1755a6', '#d63e3e', '#aa91db', '#4f23a1']`

**Statistical Methods**:
- **Kruskal-Wallis**: Non-parametric test for differences among multiple groups
- **Mann-Whitney U**: Non-parametric test for pairwise comparisons (two-sided)

---

### `metaanalysis.xlsx`
**Purpose**: Excel spreadsheet containing raw meta-analysis data.

**Description**:
- Contains BV recurrence data for different intervention categories
- Used as source data for generating `metaanalysisdatatoplot.csv`
- May include multiple studies, sample sizes, and effect sizes

**Note**: This file may need to be processed to create the CSV input for `metaanalysisplot.py`.

---

## Workflow

1. **Prepare data**: Ensure `metaanalysisdatatoplot.csv` contains properly formatted percentage data
2. **Run analysis**: Execute `metaanalysisplot.py` to generate statistical tests and visualization
3. **Interpret results**: Review box plots and statistical output to assess differences between intervention categories

## Key Research Question

**How do different intervention strategies affect BV recurrence rates?**

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `scipy` (statistical tests: kruskal, mannwhitneyu)
- `itertools` (for pairwise combinations)

