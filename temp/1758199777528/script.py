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

# 1. Create wavenumber data
wavenumber = np.linspace(4000, 400, 1000)

# 2. Simulate characteristic peaks
# Define peak positions and intensities
peak_positions = {
    "O-H stretch": 3300,
    "C=O stretch": 1720,
    "C-H aromatic": 3000,
    "C=C aromatic": 1600,
}

peak_intensities = {
    "O-H stretch": 0.6,  # Broad, moderate intensity
    "C=O stretch": 0.9,  # Strong
    "C-H aromatic": 0.3,  # Weak
    "C=C aromatic": 0.4   # Moderate
}


# Create a function to simulate a Gaussian peak
def gaussian(x, mu, sigma, amplitude):
    return amplitude * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

# Simulate the spectrum by summing the Gaussian peaks
absorbance = np.zeros_like(wavenumber)
for peak_name, peak_pos in peak_positions.items():
    sigma = 20  # Peak width (adjust as needed)
    amplitude = peak_intensities[peak_name]
    absorbance += gaussian(wavenumber, peak_pos, sigma, amplitude)

# Add some baseline noise
noise_level = 0.02
noise = np.random.normal(0, noise_level, len(wavenumber))
absorbance += noise

# Invert the absorbance to simulate transmittance
transmittance = 1 - absorbance



# 3. Plot the spectrum
plt.figure(figsize=(10, 6)) # Adjust figure size for better readability

plt.plot(wavenumber, transmittance)
plt.xlabel("Wavenumber (cm^-1)")
plt.ylabel("Transmittance")
plt.title("Simulated FTIR Spectrum of Ibuprofen")
plt.xlim(4000, 400)  # Reverse x-axis for FTIR convention
plt.ylim(0, 1.1) # Set y-axis limits
plt.grid(True, linestyle='--', alpha=0.5)


# Annotate the peaks
for peak_name, peak_pos in peak_positions.items():
    plt.annotate(peak_name,
                 xy=(peak_pos, transmittance[np.argmin(np.abs(wavenumber - peak_pos))]),
                 xytext=(peak_pos + 50, transmittance[np.argmin(np.abs(wavenumber - peak_pos))] + 0.1), # Adjust text position as needed
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 horizontalalignment='left',
                 verticalalignment='bottom')




# 4. Display the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758199777528/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory


# Peak assignment table (print to console for convenience)
print("\nKey Peaks and Assignments:")
print("-" * 30)
print("{:<15} {:<15}".format("Wavenumber (cm^-1)", "Assignment"))
print("-" * 30)
for peak_name, peak_pos in peak_positions.items():
    print("{:<15} {:<15}".format(peak_pos, peak_name))

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758199777528/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
