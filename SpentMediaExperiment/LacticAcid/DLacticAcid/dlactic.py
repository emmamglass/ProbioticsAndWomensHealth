import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind
from matplotlib import cm

# 1. Define your three groups
inhibitory_dlac   = [53.472, 21.192, 78.059, 25.016]
moderate_dlac    = [17.643, 1.793, 1.476, 3.156]
uninhibitory_dlac  = [1.678, 1.483, 1.640, 1.052]

# 2. Group labels and data in order
order = ['Uninhibitory', 'Moderate', 'Inhibitory']
data  = {
    'Inhibitory':    inhibitory_dlac,
    'Moderate':          moderate_dlac,
    'Uninhibitory':  uninhibitory_dlac
}

# 3. Compute means and SEMs
means = np.array([np.mean(data[g]) for g in order])
sems  = np.array([np.std(data[g], ddof=1)/np.sqrt(len(data[g])) for g in order])

# 4. Pairwise p-values (Welch’s t-test)
pairs = [
    ('Inhibitory', 'Moderate'),
    ('Inhibitory', 'Uninhibitory'),
    ('Moderate',       'Uninhibitory')
]
pairwise_p = {}
for a, b in pairs:
    _, p = ttest_ind(data[a], data[b], equal_var=False, alternative='greater')
    pairwise_p[(a, b)] = p
print(pairwise_p)
# 5. Plot bars with pure matplotlib
plt.style.use('default')
fig, ax = plt.subplots(figsize=(8,6))

# choose 3 distinct colors from a matplotlib colormap
colors = ['#d9f3ff', '#73b6e0','#0a65a1']

bars = ax.bar(
    order,
    means,
    yerr=sems,
    capsize=5,
    color=colors,
    edgecolor='black'
)

# 6. Add pairwise significance bars
y_max = (means + sems).max()
h = (y_max - means.min()) * 0.4

for idx, ((a, b), p) in enumerate(pairwise_p.items()):
    x1, x2 = order.index(a), order.index(b)
    y = y_max + h * (idx + 1)
    # draw the line
    ax.plot([x1, x1, x2, x2],
            [y - h*0.2, y, y, y - h*0.2],
            lw=1.5, color='black')
    # choose significance string
    if p < 0.0001:
        sig = "****"
    elif p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"
    ax.text((x1 + x2) / 2, y, sig,
            ha='center', va='bottom', fontsize=12)

# 7. Labels and formatting
ax.set_ylabel('D-lactic acid concentration (mmol/L)', fontsize=12)
ax.set_title('', fontsize=14)

# remove top and right spines (despine)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# tighten layout
plt.tight_layout()
plt.show()