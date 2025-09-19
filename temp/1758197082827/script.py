import numpy as np
import matplotlib.pyplot as plt

# 1. Create wavenumber data
wavenumber = np.linspace(4000, 400, 1000)

# 2. Simulate characteristic peaks for ibuprofen
absorbance = np.zeros_like(wavenumber)

# O-H stretch
peak_center = 3300
peak_width = 50  # Adjust for peak broadness
peak_height = 0.8
absorbance += peak_height * np.exp(-((wavenumber - peak_center)**2) / (2 * peak_width**2))

# C=O stretch
peak_center = 1720
peak_width = 15
peak_height = 1.0
absorbance += peak_height * np.exp(-((wavenumber - peak_center)**2) / (2 * peak_width**2))

# C-H aromatic
peak_center = 3000
peak_width = 20
peak_height = 0.3
absorbance += peak_height * np.exp(-((wavenumber - peak_center)**2) / (2 * peak_width**2))

# C=C aromatic
peak_center = 1600
peak_width = 15
peak_height = 0.5
absorbance += peak_height * np.exp(-((wavenumber - peak_center)**2) / (2 * peak_width**2))


# Add some baseline noise (optional)
noise_level = 0.02
absorbance += np.random.normal(0, noise_level, size=len(wavenumber))
absorbance = np.clip(absorbance, 0, 1.2) # Ensure absorbance doesn't go below zero or excessively high


# 3. Plot the spectrum
plt.figure(figsize=(10, 6))
plt.plot(wavenumber, absorbance, color='blue')
plt.xlabel('Wavenumber (cm⁻¹)')
plt.ylabel('Absorbance')
plt.title('Simulated FTIR Spectrum of Ibuprofen')
plt.xlim(4000, 400)  # Reverse x-axis for FTIR convention
plt.grid(True)

# 4. Display the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758197082827/plot.png', dpi=150, bbox_inches='tight')

# Table of Key Peaks (as a comment for easy copy-pasting)

# | Wavenumber (cm⁻¹) | Assignment           |
# |--------------------|----------------------|
# | ~3300              | O-H stretch          |
# | ~1720              | C=O stretch          |
# | ~3000              | C-H aromatic stretch |
# | ~1600              | C=C aromatic stretch |

# Try to extract data for frontend
import json
try:
    # Look for common variable names that might contain plot data
    data_to_extract = {}
    
    # Check for common variable names
    if 'wavenumber' in locals() and 'absorbance_formulation' in locals():
        data_to_extract = {
            'x': wavenumber.tolist() if hasattr(wavenumber, 'tolist') else list(wavenumber),
            'y': absorbance_formulation.tolist() if hasattr(absorbance_formulation, 'tolist') else list(absorbance_formulation)
        }
    elif 'x' in locals() and 'y' in locals():
        data_to_extract = {
            'x': x.tolist() if hasattr(x, 'tolist') else list(x),
            'y': y.tolist() if hasattr(y, 'tolist') else list(y)
        }
    
    if data_to_extract:
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758197082827/data.json', 'w') as f:
            json.dump(data_to_extract, f)
except Exception as e:
    print(f"Could not extract data: {e}")
