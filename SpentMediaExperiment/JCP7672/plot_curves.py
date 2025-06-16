import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

# Load datasets
df1 = pd.read_csv("Final.csv")
df2 = pd.read_csv("PGY_mcur_final.csv")

# Extract duration columns
duration1 = df1.iloc[:, 0]
duration2 = df2.iloc[:, 0]

# Define custom colors (map to base names, not including SM)
custom_colors = {"PGY (Modified)": "#050723", "A. christensenii": "#ac5b39",
                 "F. vaginae": "#ac9a39", "A. tetradius": "#7fac39",
                 "E. massiliensis": "#40ac39", "C. bergeronii": "#39ac70",
                 "A. marseille": "#39a8ac", "L. jensenii": '#396aac',
                 "A. lactolyticus": "#4639ac", "P. vaginalis": "#8539ac", 
                 "V. bacterium": "#ac3994", "M. curtisii": "#ac3955"}

# Helper function to clean column names to match custom_colors keys
def extract_base_condition(col_name):
    # Remove replicate suffixes and " SM" if present
    base = col_name.rsplit(' ', 1)[0]  # Removes replicate numbers
    if base.endswith(' SM'):
        base = base[:-3]
    return base.strip()

# Initialize dictionaries to store mean and std error
mean_values1, std_error1 = {}, {}
mean_values2, std_error2 = {}, {}

# Compute mean and standard error for df1
for col_base in custom_colors.keys():
    cols = [col for col in df1.columns if extract_base_condition(col) == col_base]
    if cols:
        mean_values1[col_base] = df1[cols].mean(axis=1)
        std_error1[col_base] = df1[cols].sem(axis=1)

# Compute mean and standard error for df2
for col_base in custom_colors.keys():
    cols = [col for col in df2.columns if extract_base_condition(col) == col_base]
    if cols:
        mean_values2[col_base] = df2[cols].mean(axis=1)
        std_error2[col_base] = df2[cols].sem(axis=1)

# Plot
plt.figure(figsize=(10, 6))

for condition, color in custom_colors.items():
    if condition in mean_values1:
        plt.plot(duration1, mean_values1[condition], label=f"{condition}", color=color, linestyle='-')
        plt.fill_between(duration1, mean_values1[condition]-std_error1[condition], mean_values1[condition]+std_error1[condition], color=color, alpha=0.2)
    if condition in mean_values2:
        plt.plot(duration2, mean_values2[condition], label=f"{condition}", color=color, linestyle='-')
        plt.fill_between(duration2, mean_values2[condition]-std_error2[condition], mean_values2[condition]+std_error2[condition], color=color, alpha=0.2)

plt.xlabel('Time (Hours)')
plt.ylabel('OD 600')
plt.title("Gardnerella vaginalis 14018 - Combined")
handles, labels = plt.gca().get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
plt.legend(unique_labels.values(), unique_labels.keys(), bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()