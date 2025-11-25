# Reaction Analysis

This folder contains scripts for analyzing metabolic reactions and subsystems to identify differences between commensal, pathogenic, and probiotic bacteria.

## Files

### `ReactionAnalysisUpsetPlot.py`
**Purpose**: Creates UpSet plots to visualize reaction set intersections between bacterial groups.

**Functionality**:
- Reads reaction lists from CSV files for each bacterial group:
  - Probiotic reactions (`Probiotic_rxn_anno.csv`)
  - Pathogen reactions (`Pathogen_rxn_anno.csv`)
  - Commensal reactions (`Commensal_rxn_anno.csv`)
- Calculates set intersections:
  - Unique to each group
  - Shared between pairs (Probiotic-Pathogen, Probiotic-Commensal, Pathogen-Commensal)
  - Shared among all three groups
- Creates UpSet plot visualization showing:
  - Set sizes for each intersection
  - Counts for each combination
- Prints unique reactions for each pairwise comparison

**Usage**:
```bash
python ReactionAnalysisUpsetPlot.py
```

**Input Files Required**:
- `Probiotic_rxn_anno.csv` - CSV with 'Reaction' column listing probiotic reactions
- `Pathogen_rxn_anno.csv` - CSV with 'Reaction' column listing pathogen reactions
- `Commensal_rxn_anno.csv` - CSV with 'Reaction' column listing commensal reactions

**Output**:
- UpSet plot visualization showing reaction set intersections
- Console output listing unique reactions for:
  - Pathogen/Commensal (reactions in pathogens but not commensals)
  - Probiotic/Commensal (reactions in probiotics but not commensals)
  - Probiotic/Pathogen (reactions in probiotics but not pathogens)

---

### `ReactionAnnotation.py`
**Purpose**: Annotates reactions with KEGG pathway information from ModelSEED and KEGG databases.

**Functionality**:
- Reads reaction names from input text files
- Queries ModelSEED database to find KEGG reaction IDs
- Queries KEGG database to retrieve metabolic pathway annotations
- Extracts "Metabolism" category information from KEGG entries
- Handles missing annotations (assigns "NA")
- Saves annotated reactions to CSV files

**Usage**:
```bash
python ReactionAnnotation.py
```

**Input Files Required**:
- `Unique_commensal_rxns.txt` - List of unique commensal reactions
- `Unique_probiotic_rxns.txt` - List of unique probiotic reactions
- `Unique_pathogen_rxns.txt` - List of unique pathogen reactions

**Output Files**:
- `Unique_commensal_anno.csv` - Annotated commensal reactions
- `Unique_probiotic_anno.csv` - Annotated probiotic reactions
- `Unique_pathogen_anno.csv` - Annotated pathogen reactions

**Note**: This script makes API calls to ModelSEED and KEGG databases, which may take time for large reaction lists.

**Dependencies**:
- `requests` - For API calls
- `Bio` (Biopython) - For KEGG database access
- `cobra` - For SBML model reading (if needed)

---

### `subsystem_differences_hist.py`
**Purpose**: Creates bar charts comparing metabolic subsystem distributions between bacterial groups.

**Functionality**:
- Reads annotated reaction files for pairwise comparisons:
  - Pathogen vs. Commensal (`Pathogens_Commensals_annot.csv`)
  - Probiotic vs. Pathogen (`Probiotic_Pathogen_annot.csv`)
  - Probiotic vs. Commensal (`Probiotic_Commensal_annot.csv`)
- Extracts annotation (subsystem) information
- Counts reactions per subsystem
- Sorts subsystems by frequency
- Creates three side-by-side bar charts showing:
  - Percentage of reactions in each subsystem
  - For reactions shared between each pair of groups

**Usage**:
```bash
python subsystem_differences_hist.py
```

**Input Files Required**:
- `Pathogens_Commensals_annot.csv` - Annotated reactions shared between pathogens and commensals
- `Probiotic_Pathogen_annot.csv` - Annotated reactions shared between probiotics and pathogens
- `Probiotic_Commensal_annot.csv` - Annotated reactions shared between probiotics and commensals

Each CSV should contain an 'Annotation' column with subsystem information.

**Output**:
- Three-panel bar chart showing subsystem distributions for:
  - Pathogen/Commensal comparison
  - Pathogen/Probiotic comparison
  - Commensal/Probiotic comparison

---

### `Unique_subystem_comparison.py`
**Purpose**: Creates horizontal bar charts comparing unique metabolic subsystems for each bacterial group.

**Functionality**:
- Reads annotated reaction files for unique reactions:
  - Unique Commensal (`Unique_commensal_anno.csv`)
  - Unique Pathogen (`Unique_pathogen_anno.csv`)
  - Unique Probiotic (`Unique_probiotic_anno.csv`)
- Extracts annotation (subsystem) information
- Counts reactions per subsystem
- Sorts subsystems by frequency
- Creates three stacked horizontal bar charts showing:
  - Number of unique reactions in each subsystem
  - Color-coded by group (Commensal: blue, Pathogen: orange, Probiotic: green)

**Usage**:
```bash
python Unique_subystem_comparison.py
```

**Input Files Required**:
- `Unique_commensal_anno.csv` - Annotated unique commensal reactions
- `Unique_pathogen_anno.csv` - Annotated unique pathogen reactions
- `Unique_probiotic_anno.csv` - Annotated unique probiotic reactions

Each CSV should contain an 'Annotation' column with subsystem information.

**Output**:
- Three-panel horizontal bar chart showing:
  - Unique Commensal Reaction Subsystems (blue)
  - Unique Pathogen Reaction Subsystems (orange)
  - Unique Probiotic Reaction Subsystems (green)

**Color Scheme**:
- Commensal: `#167DCC` (blue)
- Pathogen: `#E4A358` (orange)
- Probiotic: `#3C7F4D` (green)

---

## Workflow

1. **Identify unique reactions**: Extract reactions unique to each bacterial group
2. **Annotate reactions**: Run `ReactionAnnotation.py` to get KEGG pathway annotations
3. **Visualize intersections**: Run `ReactionAnalysisUpsetPlot.py` to see reaction overlaps
4. **Compare subsystems**: 
   - Run `subsystem_differences_hist.py` for shared reactions
   - Run `Unique_subystem_comparison.py` for unique reactions

## Key Research Questions

1. **What reactions are unique to each bacterial group?**
2. **What metabolic subsystems are enriched in each group?**
3. **How much metabolic overlap exists between groups?**

## Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `upsetplot` - For UpSet plot visualization
- `requests` - For API calls (ReactionAnnotation.py)
- `Bio` (Biopython) - For KEGG access (ReactionAnnotation.py)
- `cobra` - For SBML model reading (ReactionAnnotation.py)

