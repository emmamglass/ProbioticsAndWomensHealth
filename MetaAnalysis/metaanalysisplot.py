import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.stats import kruskal, mannwhitneyu

# Load and preprocess data
df = pd.read_csv('metaanalysisdatatoplot.csv')
# Melt DataFrame into long format
df_long = df.melt(var_name='Category', value_name='Value')
# Convert percentage strings to numeric and drop missing
df_long['Value'] = pd.to_numeric(df_long['Value'].str.rstrip('%'), errors='coerce')
df_long = df_long.dropna(subset=['Value'])

# Prepare data for plotting and statistics
categories = df_long['Category'].unique().tolist()
data_groups = [df_long[df_long['Category'] == cat]['Value'] for cat in categories]

# Overall non-parametric test (Kruskal-Wallis)
H_stat, p_overall = kruskal(*data_groups)
print(f"Kruskal-Wallis H-statistic: {H_stat:.3f}, p-value: {p_overall:.3e}")

# Pairwise comparisons (Mann-Whitney U)
pairwise_p = {}
for a, b in itertools.combinations(categories, 2):
    data_a = df_long[df_long['Category'] == a]['Value']
    data_b = df_long[df_long['Category'] == b]['Value']
    _, p_val = mannwhitneyu(data_a, data_b, alternative='two-sided')
    pairwise_p[(a, b)] = p_val
    print(f"Comparison {a} vs {b}: p-value = {p_val:.3e}")

colors = ['#79a6e0','#1755a6','#d63e3e', '#aa91db', '#4f23a1', ]
# Plot boxplots
fig, ax = plt.subplots(figsize=(8, 6))
positions = range(1, len(categories) + 1)
bp=ax.boxplot(data_groups, positions=positions, widths=0.6, patch_artist=True, medianprops=dict(color='black'))
# Apply specified colors
for box, color in zip(bp['boxes'], colors):
    box.set_facecolor(color)
ax.set_xticks(positions)
ax.set_xticklabels(categories, rotation=45, ha='right')
ax.set_ylabel('% BV Recurrence (%)')

# Annotate significance bars
y_max = max(group.max() for group in data_groups)
y_min = min(group.min() for group in data_groups)
h = (y_max - y_min) * 0.1

for idx, ((a, b), p_val) in enumerate(pairwise_p.items()):
    x1 = categories.index(a) + 1
    x2 = categories.index(b) + 1
    y = y_max + h * (idx + 1)
    ax.plot([x1, x1, x2, x2], [y - h*0.2, y, y, y - h*0.2], lw=1.5, color='black')
    # Determine significance level notation
    if p_val < 0.001:
        sig = '***'
    elif p_val < 0.01:
        sig = '**'
    elif p_val < 0.05:
        sig = '*'
    else:
        sig = 'ns'
    ax.text((x1 + x2) / 2, y, sig, ha='center', va='bottom')

plt.tight_layout()
plt.show()