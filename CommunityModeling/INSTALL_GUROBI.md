# Installing Gurobi for MICOM

MICOM's `cooperative_tradeoff` function requires a QP (Quadratic Programming) solver. GLPK only supports linear programming, so you need Gurobi or CPLEX.

## Option 1: Install Gurobi (Recommended)

### Step 1: Get Academic License (Free)
1. Go to https://www.gurobi.com/academia/academic-program-and-licenses/
2. Sign up for a free academic license
3. You'll receive a license key via email

### Step 2: Install Gurobi
```bash
# Install gurobipy package
pip install gurobipy

# Or if using conda
conda install -c gurobi gurobi
```

### Step 3: Activate License
```bash
# Run the grbgetkey command with your license key
grbgetkey YOUR_LICENSE_KEY

# Or set environment variable
export GRB_LICENSE_FILE=/path/to/gurobi.lic
```

### Step 4: Update Script
The script will automatically detect Gurobi if installed. You can also explicitly set it:
```bash
export MICOM_SOLVER=gurobi
python pairwise_community_modeling.py
```

## Option 2: Use Linear Approximation (Current Fallback)

The script now includes a fallback that uses a linear approximation when Gurobi is not available. This is less accurate but will work with GLPK.

## Option 3: Install CPLEX (Alternative)

CPLEX is another QP-capable solver:
1. Get academic license from IBM
2. Install: `pip install cplex`
3. Set: `export MICOM_SOLVER=cplex`

## Verification

To check if Gurobi is installed and working:
```python
import gurobipy as gp
print("Gurobi version:", gp.gurobi.version())
```

