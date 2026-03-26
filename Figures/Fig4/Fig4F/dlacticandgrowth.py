import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Input data
x = np.array([6.812, 7.074, 7.116, 7.055, 5.696, 5.393, 5.886, 6.315, 2.442, 1.667, 1.315, 1.999])
y = np.array([1.678, 1.483, 1.64, 1.052, 17.643, 1.793, 1.476, 3.156, 53.472, 21.192, 78.059, 25.016])

# Define point-specific colors
point_colors = ['#d9f3ff','#d9f3ff','#d9f3ff','#d9f3ff',
                '#73b6e0','#73b6e0','#73b6e0','#73b6e0',
                '#0a65a1','#0a65a1','#0a65a1','#0a65a1']


# Define exponential model
def exp_func(x, a, b):
    return a * np.exp(b * x)

# Fit the model
params, _ = curve_fit(exp_func, x, y, p0=(1, -0.5))
a, b = params

# Predict values and calculate R²
y_pred = exp_func(x, a, b)
r2 = r2_score(y, y_pred)

# Print the equation and R²
print(f"Exponential fit equation: y = {a:.3f} * e^({b:.3f} * x)")
print(f"R² = {r2:.4f}")

# Plotting
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color=point_colors, s=150, edgecolors='black',zorder=2)
x_fit = np.linspace(min(x), max(x), 100)
y_fit = exp_func(x_fit, a, b)
plt.plot(x_fit, y_fit, color='black', linewidth=2.5, zorder=1)
plt.xlabel('G. vaginalis AUC')
plt.ylabel('D-lactic acid concentration (mmol/L)')
plt.title('')
plt.tight_layout()
plt.show()


