import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.preprocessing import MinMaxScaler

# 1. Define your lists of filenames, now including Gardnerella vaginalis
list_files = {
    'Probiotic':               'vaginal_probiotic.txt',
    'Uninhibitory':            'uninhibitory_vag_comm.txt',
    'Inhibitory':              'inhibitory_vag_comm.txt',
    'Gardnerella vaginalis':   'gardnerella_vaginalis.txt'
}

# 2. Read each file, compute median flux per reaction
median_dict = {}
group_map = {}
for group, list_path in list_files.items():
    with open(list_path, 'r') as f:
        files = [line.strip().lstrip('./') for line in f if line.strip()]
    for fn in files:
        df = pd.read_csv(fn)
        median_dict[fn] = df.median(axis=0)
        # assign grouping: Probiotic stays, Uninhibitory/Inhibitory → Commensal,
        # Gardnerella vaginalis stays its own group
        if group == 'Probiotic':
            grp = 'Probiotic'
        elif group == 'Gardnerella vaginalis':
            grp = 'Gardnerella vaginalis'
        else:
            grp = 'Commensal'
        group_map[fn] = grp

# 3. Build DataFrame; missing → 0
median_df = pd.DataFrame.from_dict(median_dict, orient='index').fillna(0)

# 3b. Save list of all reactions BEFORE filtering (strip '_c')
all_rxns = [col.rstrip('_c') for col in median_df.columns]
with open('all_reactions.txt', 'w') as f:
    for rxn in all_rxns:
        f.write(rxn + '\n')
#print(f"Saved {len(all_rxns)} reactions to all_reactions.txt")

# 3c. Absolute values
#median_df = median_df.abs()

# ─── 4. Filtering ───────────────────────────────────────────────────────────────

# 4a. Remove low‐variance reactions
var_threshold = 0.1
variances = median_df.var(axis=0)
low_var_cols = variances[variances < var_threshold].index
median_df = median_df.drop(columns=low_var_cols)
print(f"Dropped {len(low_var_cols)} low‐variance reactions")

# 4b. Remove highly correlated reactions
corr_threshold = 0.9
corr_matrix = median_df.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [col for col in upper.columns if any(upper[col] > corr_threshold)]
median_df = median_df.drop(columns=to_drop)
print(f"Dropped {len(to_drop)} reactions for high correlation")

# ─── X. Rename files → species ────────────────────────────────────────────────
# load your mapping CSV (expecting columns “file_name,species”)
species_df = pd.read_csv('file_species_mapping.csv', dtype=str)
species_map = dict(zip(species_df['file_name'], species_df['species']))

# rename the rows in median_df
new_index = [species_map.get(fn, fn) for fn in median_df.index]
median_df.index = new_index

# also rename your group_map Series so row_colors still aligns
group_series = pd.Series(group_map)
group_series.index = [species_map.get(fn, fn) for fn in group_series.index]
group_series = group_series.reindex(median_df.index)

# ─── 5. Row colors ────────────────────────────────────────────────────────────
palette = {'Probiotic': '#437a51', 'Commensal': '#095e9e', 'Gardnerella vaginalis': '#e8b723'}
row_colors = group_series.map(palette)

# ─── 6a. Load subsystem mapping, force everything to str and fill missing ────
subs_df = pd.read_csv('all_reactions.csv', dtype=str)  
subs_df['subsystem'] = subs_df['subsystem'].fillna('Unknown')
subs_map = dict(zip(subs_df['reaction'], subs_df['subsystem']))


# 6b. Build col_colors for each reaction column
# 6b. Build col_subsys for each reaction column, defaulting to 'Unknown'
col_subsys = []
for col in median_df.columns:
    rxn = col.rstrip('_c')
    subsys = subs_map.get(rxn, 'Unknown')
    # in case it's still None or nan-like
    if not isinstance(subsys, str) or subsys.strip() == '':
        subsys = 'Unknown'
    col_subsys.append(subsys)

unique_subsys = sorted(set(col_subsys))
# pick a color for each subsystem
subsys_palette = dict(zip(
    unique_subsys,
    sns.color_palette('tab20', len(unique_subsys))
))
col_colors = [subsys_palette[s] for s in col_subsys]

# ─── 7. Plot clustered heatmap with both row & col color strips ───────────────

sns.set(context='notebook', style='white')
g = sns.clustermap(
    median_df,
    metric='canberra',
    method='average',
    cmap='PuOr',
    vmin=-1000, vmax=1000,
    dendrogram_ratio=(0.1, 0),
    cbar_pos=None,
    row_colors=row_colors,
    figsize=(10, 12),
)

# 8. Label axes
g.ax_heatmap.set_xlabel('Reactions', fontweight='bold', fontsize =14 )           # name of x-axis
#g.ax_heatmap.set_ylabel('Strain Name') # name of y-axis

# 9. Remove the individual x-tick labels
g.ax_heatmap.tick_params(axis='x', which='both', labelbottom=False)

g.ax_heatmap.tick_params(
    axis='y',         # apply to the x axis
    which='major',    # major ticks
    labelsize=12,      # font size in points
)

plt.show()

# ─── 8. Legend for subsystems ─────────────────────────────────────────────────

handles = [
    mpatches.Patch(color=subsys_palette[s], label=s)
    for s in unique_subsys
]
'''g.ax_col_dendrogram.legend(
    handles=handles,
    title='Subsystem',
    bbox_to_anchor=(1.02, 1),
    loc='upper left'
)'''



