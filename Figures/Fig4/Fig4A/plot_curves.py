import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

#load dataset
df = pd.read_csv("Final.csv")

#extract duration column
duration = df.iloc[:, 0]

#identify unique condition names (excluding replicates)
conditions = list(set(col.rsplit(' ', 1)[0] for col in df.columns[1:]))
print(conditions)

#initalize dictionary to store mean and standard error
mean_values = {}
std_error = {}

#define custom colors
'''custom_colors = {"PGY (Modified)": "#050723", "A. christensenii": "#07314A",
				 "F. vaginae":"#067460", "A. tetradius":"#02A22A",
				 "E. massiliensis":"#41CC00", "C. bergeronii":"#D8F500",
				 "A. marseille":"#FF9A1F", "L. jensenii":'#FF4747',
				 "A. lactolyticus":"#FF70C1", "P. vaginalis":"#B08FFF", 
				 "V. bacterium":"#7A83FF", "M. curtsii":"#2E43FF"}'''

custom_colors = {"PGY (Modified)": "#050723", "A. christensenii": "#ac5b39",
				 "F. vaginae":"#ac9a39", "A. tetradius":"#7fac39",
				 "E. massiliensis":"#40ac39", "C. bergeronii":"#39ac70",
				 "A. marseille":"#39a8ac", "L. jensenii":'#396aac',
				 "A. lactolyticus":"#4639ac", "P. vaginalis":"#8539ac", 
				 "V. bacterium":"#ac3994", "M. curtisii":"#ac3955"}

#compute mean and standard error across trials for each condition 
for condition in custom_colors.keys():
	cols = [col for col in df.columns if col.startswith(condition)]
	if cols:
		mean_values[condition] = df[cols].mean(axis=1)
		std_error[condition]=df[cols].sem(axis=1)

#plot with standard error
for condition, color in custom_colors.items():
	if condition in mean_values:
		plt.plot(duration, mean_values[condition], label = condition, color=color)
		plt.fill_between(duration, mean_values[condition]-std_error[condition], mean_values[condition]+std_error[condition],color=color, alpha=0.2)


plt.xlabel('Time (Hours)')
plt.ylabel('OD 600')
plt.title("Gardnerella vaginalis 14018")
handles, labels = plt.gca().get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
plt.legend(unique_labels.values(), unique_labels.keys(), bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()


