import numpy as np
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

# Data from the table
days = [1, 2, 3, 4, 5, 6, 7]
heights = [2, 3.5, 5, 6.5, 8, 9, 9.5]

# Create the plot
plt.figure(figsize=(8, 6))  # Adjust figure size for better viewing

plt.plot(days, heights, marker='o', linestyle='-', color='green') #creates the graph

# Add labels and title
plt.xlabel("Day")
plt.ylabel("Height (cm)")
plt.title("Plant Growth Over a Week")

# Add gridlines for better readability
plt.grid(True)

# Customize x-axis ticks to be integers
plt.xticks(days) # Ensures all days are labeled on x-axis

# Display the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758383964142/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

# Optional: Save the plot to a file
#plt.savefig("plant_growth.png")  # Saves as a PNG image

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758383964142/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
