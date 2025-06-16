import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Include Uninhibitory, Inhibitory, and Gardnerella vaginalis
list_files = {
    'Uninhibitory':            'uninhibitory_vag_comm.txt',
    'Moderate':                'moderate_vag_comm.txt',
    'Inhibitory':              'inhibitory_vag_comm.txt',
    'Gardnerella vaginalis':   'gardnerella_vaginalis.txt'
}

# 2. Compute median‐flux per reaction
median_dict = {}
group_map = {}
for group, list_path in list_files.items():
    with open(list_path, 'r') as f:
        files = [ln.strip().lstrip('./') for ln in f if ln.strip()]
    for fn in files:
        df = pd.read_csv(fn)
        median_dict[fn] = df.median(axis=0)
        group_map[fn] = group

# 3. Build DataFrame & save all reaction names
median_df = pd.DataFrame.from_dict(median_dict, orient='index').fillna(0)
all_rxns = [c.rstrip('_c') for c in median_df.columns]
with open('all_reactions.txt','w') as f:
    for rxn in all_rxns:
        f.write(rxn + '\n')
#median_df = median_df.abs()

# 4a. Drop low‐variance reactions
var_thresh = 0.1
low_var = median_df.var(axis=0) < var_thresh
median_df = median_df.drop(columns=median_df.columns[low_var])

# 4b. Drop highly correlated reactions
corr = median_df.corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
to_drop = [c for c in upper.columns if any(upper[c] > 0.9)]
median_df = median_df.drop(columns=to_drop)

# ─── X. Rename file‐names → species ─────────────────────────────────────────────
# Load mapping CSV (expects columns "file_name","species")
species_df = pd.read_csv('file_species_mapping.csv', dtype=str)
species_map = dict(zip(species_df['file_name'], species_df['species']))

# Rename the rows of median_df
new_index = [species_map.get(fn, fn) for fn in median_df.index]
median_df.index = new_index

# Prepare group_series aligned to the new species index
group_series = pd.Series(group_map)
group_series.index = [species_map.get(fn, fn) for fn in group_series.index]
group_series = group_series.reindex(median_df.index)

# 5. Row‐color strip: unique color per group
palette = {
    'Uninhibitory':          '#66B5E9',  # blue
    'Moderate':              '#3685B9',
    'Inhibitory':            '#07568A',  # orange
    'Gardnerella vaginalis': '#e8b723'   # green
}
row_colors = group_series.map(palette)

# 6a. Load reaction→subsystem mapping for column colors
subs_df = pd.read_csv('all_reactions.csv', dtype=str)
subs_df['subsystem'] = subs_df['subsystem'].fillna('Unknown')
subs_map = dict(zip(subs_df['reaction'], subs_df['subsystem']))

# 6b. Column‐color strip by subsystem
col_subsys = [subs_map.get(c.rstrip('_c'), 'Unknown') for c in median_df.columns]
unique_subsys = sorted(set(col_subsys))
subsys_palette = dict(zip(
    unique_subsys,
    sns.color_palette('tab20', len(unique_subsys))
))
col_colors = [subsys_palette[s] for s in col_subsys]

# 7. Draw clustered heatmap
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
    figsize=(10, 12)
)
# 9. Remove the individual x-tick labels
g.ax_heatmap.tick_params(axis='x', which='both', labelbottom=False)
# 8. ends
# Row legend (file/species groups)
'''row_handles = [mpatches.Patch(color=clr, label=grp) for grp, clr in palette.items()]
g.ax_heatmap.legend(
    handles=row_handles,
    title='Group',
    bbox_to_anchor=(1.02, 0.8),
    loc='upper left'
)'''
'''# Column legend (subsystems)
col_handles = [mpatches.Patch(color=subsys_palette[s], label=s) for s in unique_subsys]
g.ax_col_dendrogram.legend(
    handles=col_handles,
    title='Subsystem',
    bbox_to_anchor=(1.02, 1.02),
    loc='upper left'
)'''

# 9. Axis labels
g.ax_heatmap.set_xlabel('Reaction', fontweight='bold')
g.ax_row_dendrogram.set_ylabel(
    'Species',
    rotation=90,
    fontweight='bold',
    labelpad=40
)

g.ax_heatmap.tick_params(
    axis='y',         # apply to the x axis
    which='major',    # major ticks
    labelsize=14,      # font size in points
)


plt.show()




