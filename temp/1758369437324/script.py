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

# FT‑IR simulated data (wavenumber, absorbance)
wavenum = np.array([3300, 3350, 3320, 3300, 3100, 1654, 1520, 1450, 1237, 748])
absorb  = np.array([0.6, 0.4, 0.5, 0.3, 0.1, 0.8, 0.7, 0.4, 0.5, 0.2])

plt.figure()
plt.plot(wavenum[::-1], absorb[::-1], label='Paracetamol')
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Absorbance (a.u.)')
plt.title('Simulated FT‑IR of Paracetamol')
plt.legend()
plt.grid(True)
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369437324/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

# XRD simulated data:
theta = np.array([7,8,11,12,14,15,20])
intens = np.array([1.2,2.4,1.8,2.1,2.9,1.7,3.5])

plt.figure()
plt.stem(theta, intens, basefmt=" ")
plt.xlabel('2θ ( degrees)')
plt.ylabel('Relative Intensity (a.u.)')
plt.title('Simulated XRD Pattern of Paracetamol')
plt.grid(True)
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369437324/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369437324/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
