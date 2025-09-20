# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Data from the JSON
time = np.array([0, 1, 2, 3, 4, 6, 8, 10, 12])
cum_release = np.array([0, 12, 22, 34, 47, 61, 73, 84, 92])

# Create figure & axis
fig, ax = plt.subplots(figsize=(8, 5), tight_layout=True)

# Plot cumulative release
ax.plot(time, cum_release, marker='o', color='steelblue',
        linewidth=2, markersize=6, label='Cumulative Release')

# Annotate points
for t, r in zip(time, cum_release):
    ax.annotate(f'{r}%', xy=(t, r), xytext=(5, 5),
                textcoords='offset points', fontsize=9,
                ha='left', va='bottom')

# Axis labels and title
ax.set_xlabel('Time (h)', fontsize=12)
ax.set_ylabel('Cumulative Release (%)', fontsize=12)
ax.set_title('Dissolution Profile of Sustained‑Release Tablet', fontsize=14)

# Grid, legend, and aesthetic tweaks
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')
ax.set_xlim(-0.5, 12.5)
ax.set_ylim(0, 100)

# Show plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758247488848/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758247488848/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
