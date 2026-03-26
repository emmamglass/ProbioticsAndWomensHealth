# Community Modeling with MICOM

This folder is named for its manuscript artifact target: `Table6_MICOM` corresponds to Table 6 analyses and outputs.

This folder contains scripts and models for pairwise community modeling to compare G. vaginalis growth inhibition by safe candidates vs. BV-associated inhibitors.

## Standard README Template

- **Folder-to-manuscript mapping**: Folder name maps to the target figure/table/extended-data item.
- **Common section structure**: `Purpose`, `Scripts`, `Input Files`, `Output Files`, `Dependencies`, `Usage Notes`.

## Files

### `pairwise_community_modeling.py`
Main script for pairwise community modeling workflow.

### Model Files
- `2702.157.sbml` - Gardnerella vaginalis (pathogen)
- `109790.33.sbml` - Lactobacillus jensenii (safe candidate)
- `1284686.3.sbml` - Anaerococcus lactolyticus (BV-associated)
- `33036.3.sbml` - Anaerococcus tetradius (BV-associated)
- `82135.15.sbml` - Fannyhessea vaginae (BV-associated)

### Text Files
- `inhibitory_vag_comm.txt` - List of inhibitory vaginal commensal models
- `uninhibitory_vag_comm.txt` - List of uninhibitory vaginal commensal models
- `flux_list_vaginal_strains.txt` - List of vaginal strain models

## Workflow

The script implements a 4-step workflow:

### 1. Targeted Pairwise Selection
Compares G. vaginalis against:
- **Safe Candidate**: L. jensenii
- **BV-Associated Inhibitors**: A. lactolyticus, A. tetradius, F. vaginae

### 2. Community Construction and Simulation
- Uses MICOM to create pairwise community models
- Runs cooperative tradeoff analyses at varying initial relative abundances:
  - 1:1 (equal abundance)
  - 1:10 (G. vaginalis : Partner)
  - 10:1 (G. vaginalis : Partner)

### 3. Mechanistic Dissection
For each pair, calculates:
- **Growth Suppression**: Reduction in predicted G. vaginalis growth rate
- **Niche Overlap**: Jaccard distance of import fluxes (resource competition)
- **Metabolite Exchange**: Production fluxes of key metabolites (D-lactate, etc.)

### 4. Interpretation
- Compares metabolic profiles between safe candidates and BV-associated inhibitors
- Identifies engineering targets:
  - Minimum D-lactate production flux for maximal inhibition
  - Maximum niche overlap needed for strong competition

## Usage

### Prerequisites

Install required packages:
```bash
pip install micom cobra pandas numpy matplotlib seaborn
```

Note: MICOM requires Gurobi solver (free academic license available).
If Gurobi is not installed, the script automatically falls back to the open-source
`glpk` solver. You can override the solver by setting the `MICOM_SOLVER`
environment variable (supported options: `glpk`, `glpk_exact`, `hybrid`, `osqp`, `scipy`, or `gurobi` if installed).
Example:
```bash
export MICOM_SOLVER=gurobi   # or glpk
```

### Configuration

1. **Model Files**: Model mappings are already configured:
   ```python
   MODEL_MAPPINGS = {
       'G_vaginalis': '2702.157.sbml',
       'L_jensenii': '109790.33.sbml',
       'A_lactolyticus': '1284686.3.sbml',
       'A_tetradius': '33036.3.sbml',
       'F_vaginae': '82135.15.sbml',
   }
   ```

2. **Define Media Constraints** (optional): Update the `define_media_constraints()` function with your media composition (PGY-mod or Synthetic Vaginal Fluid).
3. **Solver Selection** (optional): To force a specific solver, set `MICOM_SOLVER`
   before running the script. Default is `glpk`.

### Running the Script

```bash
cd "/Users/eglass/Desktop/UVA/Nautre Microbiology/CommunityModeling"
python pairwise_community_modeling.py
```

### Required Inputs
- SBML models listed in `MODEL_MAPPINGS` stored in this folder.
- Text lists (`inhibitory_vag_comm.txt`, `uninhibitory_vag_comm.txt`, `flux_list_vaginal_strains.txt`) with one SBML filename per line; no headers.
- Optional media constraints: edit `define_media_constraints()` to match your media (e.g., PGY-mod, Synthetic Vaginal Fluid).

## Output

The script generates results in the `pairwise_results/` directory:

1. **`pairwise_summary.csv`**: Summary statistics for all simulations
   - Columns typically include: `pair` (partner label), `abundance_ratio` (e.g., `1:1`), `g_vaginalis_growth`, `partner_growth`, `growth_suppression`, `niche_overlap`, and `d_lactate_flux`.

2. **`detailed_results.pkl`**: Full simulation results (pickle format)
   - Complete solution objects
   - Community models
   - Metabolite exchange fluxes

3. **`pairwise_comparison_plots.png`**: Comparison visualizations
   - Growth suppression by category
   - Niche overlap comparison
   - D-lactate production
   - Growth suppression vs D-lactate correlation

4. **`abundance_dependent_effects.png`**: Abundance-dependent analysis
   - Growth suppression at different abundance ratios

## Key Metrics

### Growth Suppression
Fractional reduction in G. vaginalis growth when paired with inhibitor:
```
Growth Suppression = (G. vaginalis alone - G. vaginalis in pair) / G. vaginalis alone
```

### Niche Overlap (Jaccard Distance)
Measure of resource competition:
- **Low distance** (close to 0): High overlap, strong competition
- **High distance** (close to 1): Low overlap, weak competition

### D-Lactate Production
Production flux of D-lactate from partner organism (mmol/gDW/hr).

## Interpreting Results

### For Probiotic Selection
- **Low niche overlap + High D-lactate production** = Ideal safe probiotic candidate
- Compare L. jensenii profile to BV-associated inhibitors

### For Engineering Targets
- **Maximum D-lactate production** from BV-associated strains = Target flux for engineering
- **Minimum niche overlap** from BV-associated strains = Maximum competition needed

## Troubleshooting

### Model File Not Found
- Ensure all SBML files are in the same directory as the script
- Check `MODEL_MAPPINGS` dictionary has correct filenames

### Solver Issues
- Ensure Gurobi is installed and licensed
- Check MICOM installation: `pip install micom --upgrade`

### Memory Issues
- Reduce number of pairs or abundance ratios if needed
- Consider running simulations separately for each pair

## References

- MICOM documentation: https://micom-dev.github.io/micom/
- COBRApy documentation: https://cobrapy.readthedocs.io/

