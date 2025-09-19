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

# Generate wavenumber range from 4000 to 400 cm^-1
wavenumber = np.arange(4000, 400, -1)

# Gaussian peak shape function
def gaussian_peak(x, center, amplitude, sigma):
    return amplitude * np.exp(-(x - center)**2 / (2 * sigma**2))

# Initialize spectrum array with zeros
spectrum = np.zeros_like(wavenumber)

# Add peaks with appropriate intensities and widths
# O-H Stretch (broad peak)
sigma_oh = 150
amplitude_oh = 10
o_h_peak = gaussian_peak(wavenumber, 3300, amplitude_oh, sigma_oh)
spectrum += o_h_peak

# C=O Stretch (sharp peak)
sigma_co = 50
amplitude_co = 20
c_o_peak = gaussian_peak(wavenumber, 1720, amplitude_co, sigma_co)
spectrum += c_o_peak

# C-H Aromatic Stretch (sharp peak)
sigma_ch = 50
amplitude_ch = 15
c_h_peak = gaussian_peak(wavenumber, 3000, amplitude_ch, sigma_co)
spectrum += c_h_peak

# C=C Aromatic Stretch (sharp peak)
sigma_cc = 50
amplitude_cc = 10
c_c_peak = gaussian_peak(wavenumber, 1600, amplitude_cc, sigma_cc)
spectrum += c_c_peak

# Add a slight baseline shift and noise
baseline_drift = 0.1 * np.logspace((np.log10(wavenumber.min())), (np.log10(wavenumber.max())), 
                                  num=len(wavenumber), base=10)
spectrum += baseline_drift
spectrum += 0.5 * np.random.normal(size=len(wavenumber))

# Normalization
max_val = np.max(spectrum)
spectrum = spectrum / max_val

# Plotting the spectrum
plt.figure(figsize=(10, 6))
plt.plot(wavenumber, spectrum, linewidth=1.5, color='black')
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Relative Intensity')
plt.title('Simulated FTIR Spectrum of Ibuprofen')
plt.xlim(4000, 400)  # Ensure correct x-axis limits
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758207598211/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758207598211/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
