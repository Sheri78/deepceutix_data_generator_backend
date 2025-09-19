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
from scipy.stats import lognorm

# Significance of Particle Size in Pharmaceutical Formulations

print("""
#########################################################################
# Significance of Particle Size in Pharmaceutical Formulations:         #
#########################################################################

Particle size is a critical quality attribute (CQA) in pharmaceutical
formulations because it significantly impacts various aspects of drug
product performance and manufacturability.  Here's why:

* **Dissolution Rate:** Smaller particle sizes generally lead to a larger
  surface area, which in turn increases the rate at which a drug dissolves.
  Faster dissolution often translates to improved bioavailability and quicker
  onset of action.

* **Bioavailability:** The extent to which a drug is absorbed into the
  systemic circulation is directly influenced by particle size.  Poorly
  soluble drugs may exhibit enhanced bioavailability when formulated with
  nanoparticles or micronized particles.

* **Content Uniformity:**  For solid dosage forms like tablets and capsules,
  uniform particle size distribution ensures consistent drug content in each
  unit dose. Segregation can occur when particles have varying sizes and
  densities, leading to dose variability.

* **Flowability:** Powder flow properties are crucial for efficient
  manufacturing processes, especially in high-speed tablet compression and
  capsule filling.  Particle size and shape affect flowability, with smaller
  particles often exhibiting poorer flow characteristics due to increased
  cohesive forces.

* **Compression:** Particle size distribution influences the compressibility of
  powders. Uniform size distribution contributes to better packing and stronger
  compacts, which are essential for tablet hardness and friability.

* **Suspension Stability:**  In suspensions, particle size affects the
  sedimentation rate and redispersibility of the drug. Finer particles tend to
  settle more slowly and are easier to resuspend, leading to greater physical
  stability.

* **Aerosol Delivery:** For inhaled drug products, particle size is a primary
  determinant of lung deposition.  Particles in the respirable range (typically
  1-5 microm) are required to reach the lower airways and alveoli.

* **Taste Masking:**  Larger particle sizes can be used to mask the bitter
  taste of some drugs by reducing the surface area exposed to the taste buds.

Therefore, controlling particle size during drug development and manufacturing
is paramount to ensure product quality, efficacy, and safety.  Particle size
analysis is an essential tool for characterizing pharmaceutical powders and
optimizing formulation performance.
""")

# 1. Create Log-Normal Distribution of Particle Sizes
# Defining parameters for the log-normal distribution
shape = 0.8  # Shape parameter (sigma) - adjust for distribution shape
loc = 0      # Location parameter (usually 0)
scale = 10   # Scale parameter (median) - adjust for particle size range

# Generate particle sizes between 1 and 100 microm (inclusive)
size = 1000  # Number of particles to generate
particles = lognorm.rvs(shape, loc=loc, scale=scale, size=size)
particles = particles[(particles >= 1) & (particles <= 100)] # Filter for particles within the desired range

# Ensure we have enough particles after filtering
if len(particles) < size * 0.5:  # Adjust threshold as needed
    print(f"Warning: Only {len(particles)} particles generated after filtering. Consider adjusting distribution parameters.")

# 2. Calculate D10, D50, D90 Values

# D10: Particle size below which 10% of the particles lie
D10 = np.percentile(particles, 10)

# D50: Particle size below which 50% of the particles lie (median)
D50 = np.percentile(particles, 50)

# D90: Particle size below which 90% of the particles lie
D90 = np.percentile(particles, 90)

print(f"D10: {D10:.2f} microm")
print(f"D50 (Median): {D50:.2f} microm")
print(f"D90: {D90:.2f} microm")


# 3. Create Histogram and Cumulative Distribution Plots

# --- Histogram ---
plt.figure(figsize=(12, 6))  # Adjust figure size for better visualization
plt.subplot(1, 2, 1)  # Create a subplot (1 row, 2 columns, 1st position)
plt.hist(particles, bins=50, edgecolor='black', density=True, alpha=0.7) #Using density=True for normalized histogram
plt.title('Particle Size Distribution Histogram')
plt.xlabel('Particle Size (microm)')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--', alpha=0.5)  # Add grid for better readability

# --- Cumulative Distribution ---
plt.subplot(1, 2, 2)  # Create a subplot (1 row, 2 columns, 2nd position)

# Sort the particle sizes for creating the CDF
sorted_particles = np.sort(particles)
cumulative_probability = np.arange(1, len(sorted_particles) + 1) / len(sorted_particles)

plt.plot(sorted_particles, cumulative_probability, marker='.', linestyle='-', color='blue')
plt.title('Cumulative Distribution Function (CDF)')
plt.xlabel('Particle Size (microm)')
plt.ylabel('Cumulative Probability')
plt.grid(True, linestyle='--', alpha=0.5)
plt.ylim(0, 1.05)  # Set y-axis limits to ensure the CDF reaches 1

plt.tight_layout()  # Adjust subplot parameters for a tight layout. Prevents overlapping plots.
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758200120865/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory



# 4. Statistical Summary

mean_particle_size = np.mean(particles)
median_particle_size = np.median(particles)
std_dev_particle_size = np.std(particles)

print("\nStatistical Summary:")
print(f"Mean Particle Size: {mean_particle_size:.2f} microm")
print(f"Median Particle Size: {median_particle_size:.2f} microm")
print(f"Standard Deviation: {std_dev_particle_size:.2f} microm")

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758200120865/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
