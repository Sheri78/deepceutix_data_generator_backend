import numpy as np
import matplotlib.pyplot as plt

# 1. Wavenumber Data
wavenumber = np.linspace(4000, 400, 2000)  # Creates 2000 points

# 2. Simulate Peaks (Gaussian functions)
def gaussian(x, amplitude, center, width):
    return amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))

# Baseline (arbitrary, avoids negative transmittance)
transmittance = np.ones_like(wavenumber)

# Add characteristic peaks - adjusted amplitudes for better visual clarity
transmittance -= gaussian(wavenumber, 0.3, 3300, 50)  # O-H stretch
transmittance -= gaussian(wavenumber, 0.6, 1720, 20)  # C=O stretch
transmittance -= gaussian(wavenumber, 0.2, 3000, 30)  # C-H aromatic
transmittance -= gaussian(wavenumber, 0.15, 1600, 15) # C=C aromatic
# Add some smaller peaks to mimic the complexity of a real spectrum
transmittance -= gaussian(wavenumber, 0.05, 2900, 10) # C-H alkane
transmittance -= gaussian(wavenumber, 0.07, 1450, 10) # C-H bending
transmittance -= gaussian(wavenumber, 0.04, 1225, 10) # C-O stretch
transmittance -= gaussian(wavenumber, 0.03, 900, 5) # Aromatic ring vibration
transmittance -= gaussian(wavenumber, 0.03, 700, 5) # Aromatic ring vibration



# 3. Plotting the Spectrum
plt.figure(figsize=(10, 6)) # Adjust figure size for better viewing
plt.plot(wavenumber, transmittance, color='blue')
plt.xlabel("Wavenumber (cm⁻¹)", fontsize=12)
plt.ylabel("Transmittance (Arbitrary Units)", fontsize=12)  # Added units
plt.title("Simulated FTIR Spectrum of Ibuprofen", fontsize=14)
plt.xlim(4000, 400)  # Reverse x-axis
plt.ylim(0, 1.1)  # Set y-axis limits
plt.grid(True, linestyle='--', alpha=0.5) # Add a subtle grid
plt.tight_layout() # Prevents labels from being cut off

# Annotate key peaks
plt.annotate('O-H Stretch', xy=(3300, transmittance[np.argmin(np.abs(wavenumber - 3300))]), xytext=(3300, 0.4),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

plt.annotate('C=O Stretch', xy=(1720, transmittance[np.argmin(np.abs(wavenumber - 1720))]), xytext=(1720, 0.2),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

plt.annotate('C-H Aromatic', xy=(3000, transmittance[np.argmin(np.abs(wavenumber - 3000))]), xytext=(3000, 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

plt.annotate('C=C Aromatic', xy=(1600, transmittance[np.argmin(np.abs(wavenumber - 1600))]), xytext=(1600, 0.3),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

# 4. Display the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758198899049/plot.png', dpi=150, bbox_inches='tight')


# Table of Key Peaks (Can be displayed separately)
print("\nKey Peaks and Assignments:")
print("---------------------------")
print("Wavenumber (cm⁻¹) | Assignment")
print("---------------------------")
print("~3300            | O-H Stretch")
print("~1720            | C=O Stretch")
print("~3000            | C-H Aromatic")
print("~1600            | C=C Aromatic")
print("---------------------------")

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758198899049/data.json', 'w') as f:
            json.dump(data_to_extract, f)
except Exception as e:
    print(f"Could not extract data: {e}")
