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

# Simulated data
Tg_PLGA = 50
Tm_Paracetamol = 169.5
Degradation_Onset_Paracetamol = 210
Full_Degradation_Paracetamol = 290
Degradation_Onset_PLGA = 260
Full_Degradation_PLGA = 360

# Generate thermogram plot
T = np.linspace(0, 400, 100)
PLGA_heat_flow = np.where(T < Tg_PLGA, 0, np.where(T < Tm_Paracetamol, 0.1, 0))
Paracetamol_heat_flow = np.where(T < Tm_Paracetamol, 0, 1)

plt.plot(T, PLGA_heat_flow, label='PLGA')
plt.plot(T, Paracetamol_heat_flow, label='Paracetamol')
plt.xlabel('Temperature ( degreesC)')
plt.ylabel('Heat Flow (W/g)')
plt.title('DSC Thermogram')
plt.legend()
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369798725/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

# Generate TGA thermogram plot
T = np.linspace(0, 400, 100)
Paracetamol_weight_loss = np.where(T < Degradation_Onset_Paracetamol, 0, np.where(T < Full_Degradation_Paracetamol, 0.5, 1))
PLGA_weight_loss = np.where(T < Degradation_Onset_PLGA, 0, np.where(T < Full_Degradation_PLGA, 0.2, 1))

plt.plot(T, Paracetamol_weight_loss, label='Paracetamol')
plt.plot(T, PLGA_weight_loss, label='PLGA')
plt.xlabel('Temperature ( degreesC)')
plt.ylabel('Weight Loss (%)')
plt.title('TGA Thermogram')
plt.legend()
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369798725/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369798725/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
