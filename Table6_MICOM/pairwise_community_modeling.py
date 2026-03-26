#!/usr/bin/env python3
"""
Pairwise Community Modeling with MICOM
Compares G. vaginalis growth inhibition by safe candidates vs. BV-associated inhibitors

Workflow:
1. Targeted Pairwise Selection - Compare safe candidate vs BV-associated inhibitors
2. Community Construction and Simulation - Use MICOM with varying abundances
3. Mechanistic Dissection - Growth suppression, niche overlap, metabolite exchange
4. Interpretation - Identify engineering targets for safe strain improvement
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from micom import Community
from micom.workflows import build, grow
from cobra.io import read_sbml_model
from cobra.util import create_stoichiometric_matrix
import warnings
warnings.filterwarnings('ignore')

# Solver selection: Prefer OSQP (open-source QP solver, no license required)
# Can be overridden with MICOM_SOLVER env var
# Options: 'osqp' (default, open-source QP), 'glpk' (open-source LP), 'gurobi' (requires license)
OSQP_MIN_VERSION = (0, 6, 0)
OSQP_MAX_VERSION = (0, 9, 999)

if 'MICOM_SOLVER' in os.environ:
    DEFAULT_SOLVER = os.environ.get('MICOM_SOLVER')
    print(f"Using solver from MICOM_SOLVER env var: {DEFAULT_SOLVER}")
else:
    # Try to use OSQP by default
    try:
        import osqp
        version_tuple = tuple(int(part) for part in osqp.__version__.split('.') if part.isdigit())
        if version_tuple < OSQP_MIN_VERSION or version_tuple > OSQP_MAX_VERSION:
            raise RuntimeError(
                f"OSQP version {osqp.__version__} detected, but MICOM requires <1.0.0.\n"
                "Install OSQP 0.6.x in a Python 3.11 environment:\n"
                "  1. brew install python@3.11\n"
                "  2. python3.11 -m venv venv311 && source venv311/bin/activate\n"
                "  3. pip install 'osqp<1.0.0'\n"
            )
        DEFAULT_SOLVER = 'osqp'
        print(f"Using OSQP solver (version {osqp.__version__}) for cooperative_tradeoff")
    except (ImportError, RuntimeError) as osqp_err:
        print(f"⚠ OSQP not available ({osqp_err}). Falling back to GLPK (linear only).")
        DEFAULT_SOLVER = 'glpk'
        print("  Note: GLPK supports only linear optimization.")
        print("  For full QP support install OSQP (<1.0.0) or Gurobi.")
        try:
            import gurobipy
            print("  (Gurobi is installed - set MICOM_SOLVER=gurobi to use it.)")
        except ImportError:
            pass

# ============================================================================
# CONFIGURATION
# ============================================================================

# Define model file mappings
MODEL_MAPPINGS = {
    'G_vaginalis': '2702.157.sbml',
    'L_jensenii': '109790.33.sbml',
    'A_lactolyticus': '1284686.3.sbml',
    'A_tetradius': '33036.3.sbml',
    'F_vaginae': '82135.15.sbml',
}

# Define pairs to model (G. vaginalis vs partner)
PAIRS = [
    {
        'gv_id': 'G_vaginalis',
        'partner_id': 'L_jensenii',
        'partner_name': 'Lactobacillus jensenii',
        'category': 'Safe Candidate',
        'description': 'Safe probiotic candidate'
    },
    {
        'gv_id': 'G_vaginalis',
        'partner_id': 'A_lactolyticus',
        'partner_name': 'Anaerococcus lactolyticus',
        'category': 'BV-Associated',
        'description': 'Potent BV-associated inhibitor'
    },
    {
        'gv_id': 'G_vaginalis',
        'partner_id': 'A_tetradius',
        'partner_name': 'Anaerococcus tetradius',
        'category': 'BV-Associated',
        'description': 'Potent BV-associated inhibitor'
    },
    {
        'gv_id': 'G_vaginalis',
        'partner_id': 'F_vaginae',
        'partner_name': 'Fannyhessea vaginae',
        'category': 'BV-Associated',
        'description': 'Potent BV-associated inhibitor'
    },
]

# Initial relative abundances to test
ABUNDANCES = [
    (1.0, 1.0),   # 1:1
    (1.0, 10.0),  # 1:10 (G. vaginalis : Partner)
    (10.0, 1.0),  # 10:1 (G. vaginalis : Partner)
]

# Media constraints (can be customized)
MEDIA = 'PGY_mod'  # or 'Synthetic_Vaginal_Fluid'

# Output directory
OUTPUT_DIR = 'pairwise_results'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Solvers that typically ship with COBRA/MICOM (informational)
SUPPORTED_SOLVERS = ('glpk', 'glpk_exact', 'hybrid', 'osqp', 'scipy')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_model(filepath, model_id):
    """Load and prepare an SBML model."""
    print(f"Loading model: {filepath}")
    model = read_sbml_model(filepath)
    model.id = model_id
    return model

def set_model_solver(model, solver_id=DEFAULT_SOLVER):
    """Configure solver for a COBRA model, with helpful error message."""
    try:
        model.solver = solver_id
    except Exception as exc:
        msg = (
            f"Solver '{solver_id}' is not available in your environment. "
            "Install the solver (e.g., Gurobi) and its Python bindings, or set the "
            "MICOM_SOLVER environment variable to one of the supported open-source "
            f"options: {', '.join(SUPPORTED_SOLVERS)}."
        )
        raise RuntimeError(msg) from exc

def calculate_jaccard_distance(fluxes1, fluxes2):
    """
    Calculate Jaccard distance between two sets of import fluxes.
    Jaccard distance = 1 - Jaccard similarity
    """
    # Get import reactions (negative exchange fluxes)
    imports1 = set(fluxes1[fluxes1 < 0].index)
    imports2 = set(fluxes2[fluxes2 < 0].index)
    
    if len(imports1) == 0 and len(imports2) == 0:
        return 0.0
    
    intersection = len(imports1.intersection(imports2))
    union = len(imports1.union(imports2))
    
    if union == 0:
        return 1.0
    
    jaccard_similarity = intersection / union
    jaccard_distance = 1 - jaccard_similarity
    
    return jaccard_distance

def get_d_lactate_production(solution, model_id, solution_fluxes=None):
    """Extract D-lactate production flux from solution."""
    # Common D-lactate exchange reaction IDs
    d_lac_reactions = [
        'EX_dlac__L_e',
        'EX_d_lac__L_e',
        'EX_D_LACTATE_e',
        'EX_dlactate_e',
    ]
    
    # Use provided solution_fluxes or try to get from solution
    fluxes = solution_fluxes
    if fluxes is None:
        if solution is not None and hasattr(solution, 'fluxes') and solution.fluxes is not None:
            fluxes = solution.fluxes
        elif solution is not None and hasattr(solution, 'fluxes_by_species'):
            # Try to get fluxes for this specific model
            if model_id in solution.fluxes_by_species:
                fluxes = solution.fluxes_by_species[model_id]
    
    if fluxes is None or (hasattr(fluxes, '__len__') and len(fluxes) == 0):
        return 0.0
    
    # Check if fluxes is a Series/DataFrame with index, or a dict
    if hasattr(fluxes, 'index'):
        for rxn_id in d_lac_reactions:
            if rxn_id in fluxes.index:
                flux = fluxes[rxn_id]
                if flux < 0:  # Negative flux means production (secretion)
                    return abs(flux)
            # Also try with model suffix
            rxn_with_suffix = f"{rxn_id}__{model_id}"
            if rxn_with_suffix in fluxes.index:
                flux = fluxes[rxn_with_suffix]
                if flux < 0:
                    return abs(flux)
    elif isinstance(fluxes, dict):
        for rxn_id in d_lac_reactions:
            if rxn_id in fluxes:
                flux = fluxes[rxn_id]
                if flux < 0:
                    return abs(flux)
            rxn_with_suffix = f"{rxn_id}__{model_id}"
            if rxn_with_suffix in fluxes:
                flux = fluxes[rxn_with_suffix]
                if flux < 0:
                    return abs(flux)
    
    return 0.0

def simulate_pairwise_community(model1_path, model2_path, model1_id, model2_id, 
                                abundance1, abundance2, pair_name, media=None):
    """
    Simulate pairwise community with specified abundances.
    
    Parameters:
    -----------
    model1_path : str
        Path to G. vaginalis model
    model2_path : str
        Path to partner model
    model1_id : str
        ID for G. vaginalis
    model2_id : str
        ID for partner organism
    abundance1 : float
        Abundance of G. vaginalis
    abundance2 : float
        Abundance of partner
    pair_name : str
        Name identifier for the pair
    media : dict, optional
        Media constraints dictionary
    """
    print(f"\n{'='*60}")
    print(f"Simulating: {pair_name}")
    print(f"Abundance ratio (G. vaginalis : Partner): {abundance1}:{abundance2}")
    print(f"{'='*60}")
    
    try:
        # Load models
        model1 = load_model(model1_path, model1_id)
        model2 = load_model(model2_path, model2_id)
        
        # Set solver on individual models (use DEFAULT_SOLVER)
        print(f"Setting solver on individual models: {DEFAULT_SOLVER}")
        set_model_solver(model1, DEFAULT_SOLVER)
        set_model_solver(model2, DEFAULT_SOLVER)

        # Get G. vaginalis growth alone (baseline)
        # Optimize model - solution is stored in model.solution
        gv_solution = model1.optimize()
        
        # Get objective value from solution (standard COBRApy pattern)
        gv_alone_growth = 0.0
        if gv_solution is not None:
            solution_status = getattr(gv_solution, 'status', None)
            if solution_status == 'optimal':
                if hasattr(gv_solution, 'objective_value') and gv_solution.objective_value is not None:
                    gv_alone_growth = gv_solution.objective_value
                elif hasattr(gv_solution, 'f') and gv_solution.f is not None:
                    gv_alone_growth = gv_solution.f
        
        # Set abundances (normalized)
        total_abundance = abundance1 + abundance2
        abundances = {
            model1_id: abundance1 / total_abundance,
            model2_id: abundance2 / total_abundance
        }
        
        # Create taxonomy DataFrame for MICOM with file column
        # MICOM requires file column, but has issues with .sbml extension
        # Workaround: create temporary .xml copies
        print("Building community model...")
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp(prefix='micom_models_')
        xml_paths = []
        
        try:
            # Create temporary .xml copies of .sbml files
            for sbml_path in [model1_path, model2_path]:
                xml_filename = os.path.basename(sbml_path).replace('.sbml', '.xml')
                xml_path = os.path.join(temp_dir, xml_filename)
                shutil.copy2(sbml_path, xml_path)
                xml_paths.append(xml_path)
            
            # Create taxonomy DataFrame with full paths to .xml files
            taxonomy_data = {
                'id': [model1_id, model2_id],
                'genus': [model1_id.split('_')[0] if '_' in model1_id else model1_id, 
                         model2_id.split('_')[0] if '_' in model2_id else model2_id],
                'species': [model1_id, model2_id],
                'file': xml_paths,  # Use full paths to .xml files
                'abundance': [abundances[model1_id], abundances[model2_id]]
            }
            taxonomy_df = pd.DataFrame(taxonomy_data)
            
            # Use Community directly with full paths to .xml files
            print(f"Creating community with solver: {DEFAULT_SOLVER}")
            community = Community(taxonomy_df, solver=DEFAULT_SOLVER)
            
            # Diagnostic: Check what solver is actually being used
            print(f"Community solver: {community.solver}")
            try:
                if hasattr(community, 'models'):
                    for model_id, model in community.models.items():
                        if hasattr(model, 'solver'):
                            solver_interface = str(model.solver.interface).lower()
                            print(f"  Model {model_id} solver: {solver_interface}")
            except Exception as e:
                print(f"  Could not inspect model solvers: {e}")
            
        finally:
            # Cleanup temporary files after community is built
            # Note: We keep the directory until the function returns
            # The models are already loaded into memory
            pass
        
        # Apply media constraints if provided
        if media:
            print("Applying media constraints...")
            for model in [model1, model2]:
                for rxn_id, bound in media.items():
                    if rxn_id in model.reactions:
                        model.reactions.get_by_id(rxn_id).lower_bound = bound
        
        # Run cooperative tradeoff optimization
        # Uses linear version by default (no QP required, works with GLPK)
        # Will try QP version if Gurobi/CPLEX available, but falls back to linear
        print("Running cooperative tradeoff optimization...")
        
        # Use cooperative_tradeoff
        # Try QP version first if we have a QP-capable solver, otherwise use linear version
        solution = None
        used_linear_fallback = False
        optimization_method = "cooperative_tradeoff"
        
        # Check if we have a QP-capable solver
        has_qp_solver = False
        solver_name = str(community.solver).lower()
        
        # Check solver name string
        if 'osqp' in solver_name or 'gurobi' in solver_name or 'cplex' in solver_name:
            has_qp_solver = True
            print(f"Detected QP solver: {solver_name[:100]}")
        
        # Also check if OSQP is the default solver
        if not has_qp_solver and DEFAULT_SOLVER == 'osqp':
            try:
                import osqp
                has_qp_solver = True
                print(f"OSQP detected via DEFAULT_SOLVER (solver string: {solver_name[:100]})")
            except ImportError:
                pass
        
        # Check underlying model solvers
        if not has_qp_solver:
            try:
                if hasattr(community, 'models'):
                    for model_id, model in community.models.items():
                        if hasattr(model, 'solver'):
                            solver_interface = str(model.solver.interface).lower()
                            if 'osqp' in solver_interface or 'gurobi' in solver_interface or 'cplex' in solver_interface:
                                has_qp_solver = True
                                print(f"Detected QP solver from model {model_id}: {solver_interface}")
                                break
            except Exception as e:
                print(f"Could not check model solvers: {e}")
        
        # Try cooperative_tradeoff (works with QP solvers, falls back automatically if needed)
        try:
            if has_qp_solver:
                print("Attempting cooperative_tradeoff with QP solver...")
            else:
                print("Attempting cooperative_tradeoff (will use available solver)...")
            
            solution = community.cooperative_tradeoff(fraction=0.5)
            print("✓ Cooperative_tradeoff completed successfully")
        except Exception as e:
            error_msg = str(e).lower()
            print(f"⚠ Cooperative_tradeoff failed: {e}")
            
            # Check for license size limitation
            if 'too large' in error_msg and 'license' in error_msg:
                print("  Gurobi license limitation detected.")
            
            # Check for QP-related errors
            if 'quadratic' in error_msg or 'qp' in error_msg or 'not support' in error_msg:
                print("  QP not supported by current solver.")
                print("  Falling back to basic linear optimization...")
                used_linear_fallback = True
                optimization_method = "linear_optimization"
            else:
                print("  Falling back to basic linear optimization...")
                used_linear_fallback = True
                optimization_method = "linear_optimization"
            
            # Try basic optimize as fallback
            try:
                solution = community.optimize()
                print("✓ Linear optimization completed successfully")
            except Exception as e2:
                raise RuntimeError(
                    f"Both cooperative_tradeoff and linear optimization failed.\n"
                    f"Original error: {e}\n"
                    f"Fallback error: {e2}"
                ) from e2
        
        if solution is None:
            raise RuntimeError("Optimization returned None - solver may have failed silently")
        
        # Debug: Print solution structure
        print(f"  Solution type: {type(solution)}")
        print(f"  Solution attributes: {[attr for attr in dir(solution) if not attr.startswith('_')]}")
        
        # Extract growth rates
        if hasattr(solution, 'members') and hasattr(solution.members, 'growth_rate'):
            growth_rates = solution.members.growth_rate
        elif hasattr(solution, 'growth_rate'):
            growth_rates = solution.growth_rate
        else:
            # Try to get growth rates from community models directly
            print("  Warning: Solution doesn't have growth_rate, extracting from models...")
            growth_rates = {}
            if hasattr(community, 'models'):
                for species_id, model in community.models.items():
                    if hasattr(model, 'solution') and model.solution is not None:
                        if hasattr(model.solution, 'objective_value'):
                            growth_rates[species_id] = model.solution.objective_value
                        elif hasattr(model.solution, 'f'):
                            growth_rates[species_id] = model.solution.f
                    # Also try model.optimize() result
                    if species_id not in growth_rates and hasattr(model, 'objective'):
                        try:
                            model.optimize()
                            if hasattr(model, 'solution') and model.solution is not None:
                                if hasattr(model.solution, 'objective_value'):
                                    growth_rates[species_id] = model.solution.objective_value
                                elif hasattr(model.solution, 'f'):
                                    growth_rates[species_id] = model.solution.f
                        except:
                            pass
            growth_rates = pd.Series(growth_rates) if growth_rates else pd.Series()
        
        gv_growth = growth_rates.get(model1_id, 0.0)
        partner_growth = growth_rates.get(model2_id, 0.0)
        
        # Calculate growth suppression (fractional reduction)
        growth_suppression = 0.0
        if gv_alone_growth > 1e-6:
            growth_suppression = (gv_alone_growth - gv_growth) / gv_alone_growth
        
        # Calculate niche overlap (Jaccard distance of import fluxes)
        print("Calculating niche overlap...")
        
        # Get exchange reactions
        exchange_rxns1 = [rxn.id for rxn in model1.exchanges]
        exchange_rxns2 = [rxn.id for rxn in model2.exchanges]
        
        # Extract import fluxes (negative exchange fluxes)
        fluxes1 = pd.Series(index=exchange_rxns1, data=0.0)
        fluxes2 = pd.Series(index=exchange_rxns2, data=0.0)
        
        # Get fluxes from solution or community model
        solution_fluxes = None
        if solution is not None and hasattr(solution, 'fluxes') and solution.fluxes is not None:
            solution_fluxes = solution.fluxes
        elif solution is not None and hasattr(solution, 'fluxes_by_species'):
            # Alternative structure - get fluxes by species
            solution_fluxes = {}
            for species_id, species_fluxes in solution.fluxes_by_species.items():
                if hasattr(species_fluxes, 'items'):
                    for rxn_id, flux_val in species_fluxes.items():
                        solution_fluxes[rxn_id] = flux_val
                elif hasattr(species_fluxes, 'index'):
                    for rxn_id in species_fluxes.index:
                        solution_fluxes[rxn_id] = species_fluxes[rxn_id]
            solution_fluxes = pd.Series(solution_fluxes)
        else:
            # Try to get fluxes directly from community model
            print("  Solution doesn't have fluxes attribute, extracting from community model...")
            try:
                # Method 1: Try to get fluxes from community's internal solution
                if hasattr(community, 'solution') and community.solution is not None:
                    if hasattr(community.solution, 'fluxes'):
                        solution_fluxes = community.solution.fluxes
                        print("  Found fluxes in community.solution")
                
                # Method 2: Get fluxes from individual models in the community
                if (solution_fluxes is None or len(solution_fluxes) == 0) and hasattr(community, 'models'):
                    solution_fluxes = {}
                    for species_id, model in community.models.items():
                        # Try different ways to get fluxes from model
                        model_fluxes = None
                        
                        # Check model.solution.fluxes
                        if hasattr(model, 'solution') and model.solution is not None:
                            if hasattr(model.solution, 'fluxes'):
                                if hasattr(model.solution.fluxes, 'items'):
                                    model_fluxes = model.solution.fluxes
                                elif hasattr(model.solution.fluxes, 'index'):
                                    model_fluxes = {rxn_id: model.solution.fluxes[rxn_id] 
                                                   for rxn_id in model.solution.fluxes.index}
                        
                        # If no solution, try to get from reactions directly
                        if model_fluxes is None:
                            try:
                                model_fluxes = {rxn.id: rxn.flux for rxn in model.reactions if hasattr(rxn, 'flux')}
                            except:
                                pass
                        
                        if model_fluxes:
                            for rxn_id, flux_val in model_fluxes.items():
                                # Store with species suffix
                                full_rxn_id = f"{rxn_id}__{species_id}"
                                solution_fluxes[full_rxn_id] = flux_val
                                # Also store without suffix (for compatibility)
                                if rxn_id not in solution_fluxes:
                                    solution_fluxes[rxn_id] = flux_val
                    
                    if solution_fluxes:
                        solution_fluxes = pd.Series(solution_fluxes)
                        print(f"  Extracted {len(solution_fluxes)} fluxes from community models")
                    else:
                        solution_fluxes = None
                
                # Method 3: Try to access fluxes via community's reaction objects
                if (solution_fluxes is None or len(solution_fluxes) == 0) and hasattr(community, 'reactions'):
                    try:
                        solution_fluxes = {rxn.id: rxn.flux for rxn in community.reactions if hasattr(rxn, 'flux')}
                        solution_fluxes = pd.Series(solution_fluxes) if solution_fluxes else None
                        if solution_fluxes is not None:
                            print(f"  Extracted {len(solution_fluxes)} fluxes from community reactions")
                    except Exception as e:
                        print(f"  Could not extract from community reactions: {e}")
                        
            except Exception as e:
                print(f"  Error extracting fluxes: {e}")
                import traceback
                traceback.print_exc()
        
        if solution_fluxes is None or len(solution_fluxes) == 0:
            print("  Warning: Could not extract flux information. Using zero fluxes.")
            solution_fluxes = pd.Series(dtype=float)
        else:
            # Extract fluxes for each model
            for rxn_id in solution_fluxes.index:
                # Try exact match first
                if rxn_id in exchange_rxns1:
                    fluxes1[rxn_id] = solution_fluxes[rxn_id]
                if rxn_id in exchange_rxns2:
                    fluxes2[rxn_id] = solution_fluxes[rxn_id]
                
                # Try with species suffix (e.g., "EX_glc__D_e__G_vaginalis")
                for prefix in [f"{rxn_id}__{model1_id}", f"{rxn_id}__{model2_id}"]:
                    if prefix in solution_fluxes.index:
                        if rxn_id in exchange_rxns1:
                            fluxes1[rxn_id] = solution_fluxes[prefix]
                        if rxn_id in exchange_rxns2:
                            fluxes2[rxn_id] = solution_fluxes[prefix]
        
        niche_overlap = calculate_jaccard_distance(fluxes1, fluxes2)
        
        # Get D-lactate production from partner
        print("Analyzing metabolite exchanges...")
        d_lactate_prod = get_d_lactate_production(solution, model2_id, solution_fluxes)
        
        # Get other significant metabolite exchanges
        metabolite_exchanges = {}
        threshold = 1e-6
        if solution_fluxes is not None and len(solution_fluxes) > 0:
            for rxn_id in solution_fluxes.index:
                flux_val = solution_fluxes[rxn_id]
                if 'EX_' in rxn_id and abs(flux_val) > threshold:
                    metabolite_exchanges[rxn_id] = flux_val
        
        print(f"  G. vaginalis growth: {gv_growth:.6f}")
        print(f"  Partner growth: {partner_growth:.6f}")
        print(f"  Growth suppression: {growth_suppression:.3f}")
        print(f"  Niche overlap (Jaccard distance): {niche_overlap:.3f}")
        print(f"  D-lactate production: {d_lactate_prod:.6f}")
        
        return {
            'pair': pair_name,
            'model1_id': model1_id,
            'model2_id': model2_id,
            'abundance_ratio': f"{abundance1}:{abundance2}",
            'abundance1': abundance1,
            'abundance2': abundance2,
            'G_vaginalis_growth': gv_growth,
            'partner_growth': partner_growth,
            'G_vaginalis_alone_growth': gv_alone_growth,
            'growth_suppression': growth_suppression,
            'niche_overlap': niche_overlap,
            'd_lactate_production': d_lactate_prod,
            'metabolite_exchanges': metabolite_exchanges,
            'optimization_method': optimization_method,
            'used_linear_fallback': used_linear_fallback,
            'solution': solution,
            'community': community,
        }
        
    except Exception as e:
        print(f"Error simulating {pair_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def identify_model_files():
    """
    Verify model files exist and return mapping.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    available_files = [f for f in os.listdir(base_dir) if f.endswith('.sbml')]
    
    print(f"\nAvailable SBML files: {available_files}")
    
    # Verify all required model files exist
    file_mapping = {}
    missing_files = []
    
    for org_id, filename in MODEL_MAPPINGS.items():
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            file_mapping[org_id] = filename
            print(f"  ✓ {org_id}: {filename}")
        else:
            missing_files.append(f"{org_id} ({filename})")
            print(f"  ✗ {org_id}: {filename} - NOT FOUND")
    
    if missing_files:
        print(f"\nWarning: Missing model files:")
        for missing in missing_files:
            print(f"  - {missing}")
    
    return file_mapping

def run_all_simulations(media_constraints=None):
    """
    Run all pairwise simulations.
    
    Parameters:
    -----------
    media_constraints : dict, optional
        Dictionary of exchange reaction IDs and lower bounds for media
    """
    results = []
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Identify model files
    file_mapping = identify_model_files()
    
    # Get G. vaginalis model path
    gv_model_path = os.path.join(base_dir, MODEL_MAPPINGS['G_vaginalis'])
    
    if not os.path.exists(gv_model_path):
        print(f"Error: G. vaginalis model not found at {gv_model_path}")
        return results
    
    # Process each pair
    for pair_info in PAIRS:
        gv_id = pair_info['gv_id']
        partner_id = pair_info['partner_id']
        partner_name = pair_info['partner_name']
        category = pair_info['category']
        
        print(f"\n{'#'*60}")
        print(f"Processing pair: {gv_id} vs {partner_id}")
        print(f"Partner: {partner_name} ({category})")
        print(f"{'#'*60}")
        
        # Get partner model file
        if partner_id not in MODEL_MAPPINGS:
            print(f"Error: Model file not mapped for {partner_id}")
            print("Please update MODEL_MAPPINGS dictionary with correct filename")
            continue
        
        partner_model_file = MODEL_MAPPINGS[partner_id]
        partner_model_path = os.path.join(base_dir, partner_model_file)
        
        if not os.path.exists(partner_model_path):
            print(f"Error: Model file not found: {partner_model_path}")
            print(f"Expected file: {partner_model_file}")
            continue
        
        # Run simulations at different abundances
        for abundance1, abundance2 in ABUNDANCES:
            pair_name = f"{gv_id}_vs_{partner_id}"
            
            result = simulate_pairwise_community(
                gv_model_path,
                partner_model_path,
                gv_id,
                partner_id,
                abundance1,
                abundance2,
                pair_name,
                media=media_constraints
            )
            
            if result:
                # Add metadata
                result['partner_name'] = partner_name
                result['category'] = category
                result['description'] = pair_info['description']
                results.append(result)
    
    return results

def create_visualizations(df_summary):
    """Create visualization plots for results."""
    print("\nCreating visualizations...")
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # 1. Growth Suppression Comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Growth suppression by category
    ax1 = axes[0, 0]
    sns.boxplot(data=df_summary, x='Category', y='Growth_Suppression', ax=ax1)
    ax1.set_title('Growth Suppression: Safe Candidate vs BV-Associated', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Growth Suppression (fractional reduction)')
    ax1.set_xlabel('Partner Category')
    
    # Niche overlap comparison
    ax2 = axes[0, 1]
    sns.boxplot(data=df_summary, x='Category', y='Niche_Overlap', ax=ax2)
    ax2.set_title('Niche Overlap (Jaccard Distance)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Niche Overlap (Jaccard Distance)')
    ax2.set_xlabel('Partner Category')
    
    # D-lactate production
    ax3 = axes[1, 0]
    sns.boxplot(data=df_summary, x='Category', y='D_Lactate_Production', ax=ax3)
    ax3.set_title('D-Lactate Production', fontsize=12, fontweight='bold')
    ax3.set_ylabel('D-Lactate Production Flux')
    ax3.set_xlabel('Partner Category')
    
    # Growth suppression vs D-lactate production
    ax4 = axes[1, 1]
    for category in df_summary['Category'].unique():
        data = df_summary[df_summary['Category'] == category]
        ax4.scatter(data['D_Lactate_Production'], data['Growth_Suppression'], 
                   label=category, alpha=0.6, s=100)
    ax4.set_xlabel('D-Lactate Production Flux')
    ax4.set_ylabel('Growth Suppression')
    ax4.set_title('Growth Suppression vs D-Lactate Production', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, 'pairwise_comparison_plots.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_path}")
    plt.close()
    
    # 2. Abundance-dependent effects
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, (ab1, ab2) in enumerate(ABUNDANCES):
        ax = axes[idx]
        data = df_summary[df_summary['Abundance_Ratio'] == f"{ab1}:{ab2}"]
        
        if len(data) > 0:
            sns.barplot(data=data, x='Partner_Name', y='Growth_Suppression', 
                       hue='Category', ax=ax)
            ax.set_title(f'Abundance Ratio {ab1}:{ab2}', fontsize=11, fontweight='bold')
            ax.set_ylabel('Growth Suppression')
            ax.set_xlabel('Partner Organism')
            ax.set_ylim(0.8, 1.0)  # Set y-axis range to focus on high suppression values
            ax.tick_params(axis='x', rotation=45)
            ax.legend(title='Category')
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, 'abundance_dependent_effects.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_path}")
    plt.close()

def analyze_results(results):
    """Analyze and summarize results."""
    print(f"\n{'='*60}")
    print("ANALYZING RESULTS")
    print(f"{'='*60}")
    
    # Convert to DataFrame
    summary_data = []
    for r in results:
        summary_data.append({
            'Pair': r['pair'],
            'Partner_Name': r.get('partner_name', r['model2_id']),
            'Partner_ID': r['model2_id'],
            'Category': r.get('category', 'Unknown'),
            'Abundance_Ratio': r['abundance_ratio'],
            'G_vaginalis_Growth': r['G_vaginalis_growth'],
            'Partner_Growth': r['partner_growth'],
            'G_vaginalis_Alone_Growth': r['G_vaginalis_alone_growth'],
            'Growth_Suppression': r['growth_suppression'],
            'Niche_Overlap': r['niche_overlap'],
            'D_Lactate_Production': r['d_lactate_production'],
        })
    
    df_summary = pd.DataFrame(summary_data)
    
    # Save summary
    summary_path = os.path.join(OUTPUT_DIR, 'pairwise_summary.csv')
    df_summary.to_csv(summary_path, index=False)
    print(f"\nSummary saved to: {summary_path}")
    
    # Compare safe candidate vs BV-associated
    print("\n" + "="*60)
    print("COMPARISON: Safe Candidate vs BV-Associated")
    print("="*60)
    
    safe_candidate = df_summary[df_summary['Category'] == 'Safe Candidate']
    bv_associated = df_summary[df_summary['Category'] == 'BV-Associated']
    
    if len(safe_candidate) > 0 and len(bv_associated) > 0:
        print("\nAverage Growth Suppression:")
        print(f"  Safe Candidate: {safe_candidate['Growth_Suppression'].mean():.4f} ± {safe_candidate['Growth_Suppression'].std():.4f}")
        print(f"  BV-Associated: {bv_associated['Growth_Suppression'].mean():.4f} ± {bv_associated['Growth_Suppression'].std():.4f}")
        
        print("\nAverage Niche Overlap (Jaccard Distance):")
        print(f"  Safe Candidate: {safe_candidate['Niche_Overlap'].mean():.4f} ± {safe_candidate['Niche_Overlap'].std():.4f}")
        print(f"  BV-Associated: {bv_associated['Niche_Overlap'].mean():.4f} ± {bv_associated['Niche_Overlap'].std():.4f}")
        
        print("\nAverage D-Lactate Production:")
        print(f"  Safe Candidate: {safe_candidate['D_Lactate_Production'].mean():.6f} ± {safe_candidate['D_Lactate_Production'].std():.6f}")
        print(f"  BV-Associated: {bv_associated['D_Lactate_Production'].mean():.6f} ± {bv_associated['D_Lactate_Production'].std():.6f}")
    
    # Identify engineering targets
    print("\n" + "="*60)
    print("ENGINEERING TARGETS")
    print("="*60)
    
    if len(bv_associated) > 0:
        # Find maximum D-lactate production from BV-associated strains
        max_d_lactate = bv_associated['D_Lactate_Production'].max()
        max_d_lactate_pair = bv_associated.loc[bv_associated['D_Lactate_Production'].idxmax(), 'Partner_Name']
        print(f"\nMaximum D-Lactate Production (BV-Associated): {max_d_lactate:.6f}")
        print(f"  Achieved by: {max_d_lactate_pair}")
        print("  → This represents the target flux for engineering safe strains.")
        
        # Find minimum niche overlap for strong competition
        min_niche_overlap = bv_associated['Niche_Overlap'].min()
        min_niche_pair = bv_associated.loc[bv_associated['Niche_Overlap'].idxmin(), 'Partner_Name']
        print(f"\nMinimum Niche Overlap (BV-Associated): {min_niche_overlap:.4f}")
        print(f"  Achieved by: {min_niche_pair}")
        print("  → This represents the maximum resource competition needed for strong inhibition.")
        
        # Find maximum growth suppression
        max_suppression = bv_associated['Growth_Suppression'].max()
        max_suppression_pair = bv_associated.loc[bv_associated['Growth_Suppression'].idxmax(), 'Partner_Name']
        print(f"\nMaximum Growth Suppression (BV-Associated): {max_suppression:.4f}")
        print(f"  Achieved by: {max_suppression_pair}")
    
    # Create visualizations
    create_visualizations(df_summary)
    
    return df_summary

def define_media_constraints():
    """
    Define media constraints for simulations.
    Can be customized for PGY-mod or Synthetic Vaginal Fluid.
    """
    # Example: PGY-mod media constraints
    # Update these based on your actual media composition
    media = {
        # 'EX_glc__D_e': -10.0,  # Glucose
        # 'EX_h2o_e': -1000.0,   # Water
        # Add other media components as needed
    }
    
    # For now, return empty dict (unlimited media)
    # Update this function with actual media constraints
    return {}

def main():
    """Main execution function."""
    print("="*60)
    print("PAIRWISE COMMUNITY MODELING WITH MICOM")
    print("="*60)
    print("\nThis script models pairwise interactions between:")
    print("  - G. vaginalis (pathogen)")
    print("  - Safe candidates (L. jensenii)")
    print("  - BV-associated inhibitors (A. lactolyticus, A. tetradius, F. vaginae)")
    print("\nWorkflow:")
    print("  1. Targeted Pairwise Selection")
    print("  2. Community Construction and Simulation")
    print("  3. Mechanistic Dissection (growth suppression, niche overlap, metabolites)")
    print("  4. Interpretation (engineering targets)")
    
    # Define media constraints
    media_constraints = define_media_constraints()
    
    # Run simulations
    print("\n" + "="*60)
    print("STEP 1: RUNNING SIMULATIONS")
    print("="*60)
    results = run_all_simulations(media_constraints=media_constraints)
    
    if not results:
        print("\nNo results generated. Please check:")
        print("  1. Model files are present in the directory")
        print("  2. MODEL_MAPPINGS dictionary is correctly configured")
        print("  3. MICOM and COBRApy are properly installed")
        return
    
    # Analyze results
    print("\n" + "="*60)
    print("STEP 2: ANALYZING RESULTS")
    print("="*60)
    df_summary = analyze_results(results)
    
    # Save detailed results
    detailed_results_path = os.path.join(OUTPUT_DIR, 'detailed_results.pkl')
    pd.Series(results).to_pickle(detailed_results_path)
    print(f"\nDetailed results saved to: {detailed_results_path}")
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    print(df_summary.to_string(index=False))
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"\nAll results saved to: {OUTPUT_DIR}/")
    print("  - pairwise_summary.csv: Summary statistics")
    print("  - detailed_results.pkl: Full simulation results")
    print("  - pairwise_comparison_plots.png: Comparison visualizations")
    print("  - abundance_dependent_effects.png: Abundance-dependent analysis")

if __name__ == '__main__':
    main()

