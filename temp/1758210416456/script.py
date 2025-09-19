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
import json

# Load JSON data
json_data = '{"x": [0, 1, 2, 4, 6, 8, 10, 12], "y": [0, 15, 28, 45, 62, 75, 85, 92]}'
data = json.loads(json_data)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(data["x"], data["y"], marker='o')
plt.title('Dissolution Profile of Sustained-Release Tablet Formulation')
plt.xlabel('Time (hours)')
plt.ylabel('Cumulative Release (%)')
plt.grid(True)
plt.xticks(data["x"])
plt.ylim(0, 100)
plt.xlim(0, 12)

# Show the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758210416456/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758210416456/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
