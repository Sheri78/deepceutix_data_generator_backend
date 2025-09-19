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
time_points = [0, 1, 2, 4, 6, 8, 10, 12]
cumulative_release = [0, 15, 28, 45, 62, 75, 85, 92]

# Calculate Release Rate (Optional but informative)
release_rate = [0]  # Initial rate doesn't exist
for i in range(1, len(time_points)):
    rate = (cumulative_release[i] - cumulative_release[i-1]) / (time_points[i] - time_points[i-1])
    release_rate.append(rate)

# Create the plot
plt.figure(figsize=(10, 6))  # Adjust figure size for better readability
plt.plot(time_points, cumulative_release, marker='o', linestyle='-', color='blue', label='Cumulative Release')
# Add Release rate to plot.
#plt.plot(time_points, release_rate, marker='x', linestyle='--', color='red', label='Release Rate') # uncomment to add Release Rate

# Customize the plot
plt.title('Dissolution Profile of Sustained-Release Tablet', fontsize=16)
plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Cumulative Release (%)', fontsize=12)
plt.xlim(0, max(time_points) + 1)  # Set x-axis limits
plt.ylim(0, 100)  # Set y-axis limits
plt.xticks(np.arange(0, max(time_points) + 1, 1))  # Set specific x-axis ticks for clarity
plt.yticks(np.arange(0, 101, 10))  # Set specific y-axis ticks for clarity
plt.grid(True, linestyle='--', alpha=0.5)  # Add a grid for better readability
plt.legend()  # Show the legend

# Add annotations for key data points (Optional)
for i, (x, y) in enumerate(zip(time_points, cumulative_release)):
    plt.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", xytext=(5,5), ha='left', fontsize=8)


# Add text with the f2 value (example)
#f2_value = 65.2  # Replace with your actual f2 value calculation
#plt.text(0.7, 0.1, f'f2 = {f2_value:.2f}', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))


plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758200055751/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758200055751/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
