import os
# Limit BLAS threads to avoid resource issues
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
from scipy.integrate import simps
from scipy.stats import f_oneway, ttest_ind
import matplotlib.pyplot as plt

# 1. Load and normalize the dataset
df = pd.read_csv('Final.csv')
# Identify the time column
time_col = 'Duration (Hours)'
time = df[time_col].values
# Normalize all other columns so the global minimum is zero
measurement_cols = [col for col in df.columns if col != time_col]
global_min = df[measurement_cols].min().min()
df[measurement_cols] = df[measurement_cols] - global_min

# 2. Define species groups with new names
groups = {
    'Uninhibitory': ['PGY (Modified) Media', 'M. curtisii SM', 'V. bacterium SM', 'E. massiliensis SM'],
    'Moderate': ['P. vaginalis SM', 'A. marseille SM', 'C. bergeronii SM', 'A. christensenii SM'],
    'Inhibitory': ['F. vaginae SM', 'A. lactolyticus SM', 'A. tetradius SM', 'L. jensenii SM']
}

# 3. Compute AUC for each replicate, then mean & std per species
species_stats = []
for grp_name, species_list in groups.items():
    for prefix in species_list:
        rep_cols = [col for col in measurement_cols if col.startswith(prefix)]
        if not rep_cols:
            raise ValueError(f"No columns found for prefix '{prefix}'")
        aucs = [simps(df[col].values, time) for col in rep_cols]
        mean_auc = np.mean(aucs)
        std_auc  = np.std(aucs, ddof=1)
        species_stats.append((prefix, grp_name, mean_auc, std_auc))

species_df = pd.DataFrame(species_stats, columns=['Species', 'Group', 'MeanAUC', 'StdAUC'])

# 4. Statistical testing
g1 = species_df.loc[species_df['Group']=='Uninhibitory', 'MeanAUC']
g2 = species_df.loc[species_df['Group']=='Moderate', 'MeanAUC']
g3 = species_df.loc[species_df['Group']=='Inhibitory', 'MeanAUC']
F_stat, p_anova = f_oneway(g1, g2, g3)

from itertools import combinations
pairwise_p = {}
for a, b in combinations(groups.keys(), 2):
    pval = ttest_ind(
        species_df.loc[species_df['Group']==a, 'MeanAUC'],
        species_df.loc[species_df['Group']==b, 'MeanAUC'], alternative='greater'
    ).pvalue
    pairwise_p[(a, b)] = pval

# Print statistical results
print("One-way ANOVA:")
print(f"  F-statistic = {F_stat:.4f}, p-value = {p_anova:.4e}\n")
print("Pairwise t-tests:")
for (a, b), p in pairwise_p.items():
    print(f"  {a} vs {b}: p-value = {p:.4e}")

# 5. Plot bar chart with updated group names
order = ['Uninhibitory', 'Moderate', 'Inhibitory']
group_means = species_df.groupby('Group')['MeanAUC'].mean().reindex(order)
group_stds  = species_df.groupby('Group')['MeanAUC'].std().reindex(order)

colors = ['#d9f3ff', '#73b6e0','#0a65a1']

x = np.arange(len(order))
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(x, group_means, yerr=group_stds, capsize=5, color=colors, edgecolor='black')
ax.set_xticks(x)
ax.set_xticklabels(order)
ax.set_ylabel('Mean AUC per Species')
ax.set_title('Normalized AUC Comparison by Group')

# Add significance bars
y_max = group_means.max() + group_stds.max()
h = (y_max - group_means.min()) * 0.1
for idx, ((a, b), p) in enumerate(pairwise_p.items()):
    x1, x2 = order.index(a), order.index(b)
    y = y_max + h * (idx + 1)
    ax.plot([x1, x1, x2, x2], [y-h*0.2, y, y, y-h*0.2], lw=1.5, color='black')
    sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'ns'
    ax.text((x1+x2)/2, y, sig, ha='center', va='bottom')

# 6. Save AUC results to CSV
output_csv_path = "species_auc_values.csv"
species_df.to_csv(output_csv_path, index=False)
print(f"AUC values saved to {output_csv_path}")

plt.tight_layout()
plt.show()