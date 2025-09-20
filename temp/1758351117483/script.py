# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Create wavenumber data
wn = np.arange(4000, 400, -1)

# Simulate characteristic peaks for ibuprofen
spectrum = np.zeros_like(wn)

# O-H stretch around 3300 cm^-1
spectrum += 1.0 * np.exp(-((wn - 3300) / 50) ** 2)

# C=O stretch around 1720 cm^-1
spectrum += 0.8 * np.exp(-((wn - 1720) / 30) ** 2)

# C-H aromatic around 3000 cm^-1
spectrum += 0.6 * np.exp(-((wn - 3000) / 40) ** 2)

# C=C aromatic around 1600 cm^-1
spectrum += 0.5 * np.exp(-((wn - 1600) / 30) ** 2)

# Plot the spectrum
plt.figure(figsize=(10, 6))
plt.plot(wn, spectrum, color='black')
plt.xlim(4000, 400)
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Absorbance')
plt.title('Simulated FTIR Spectrum of Ibuprofen')
plt.grid(True)

# Add peak annotations
plt.annotate('O-H stretch', xy=(3300, 1.0), xytext=(3300, 1.2),
             arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate('C=O stretch', xy=(1720, 0.8), xytext=(1720, 1.0),
             arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate('C-H aromatic', xy=(3000, 0.6), xytext=(3000, 0.8),
             arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate('C=C aromatic', xy=(1600, 0.5), xytext=(1600, 0.7),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758351117483/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758351117483/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
