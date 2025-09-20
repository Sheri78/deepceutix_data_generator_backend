import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

import numpy as np

# 1 K-spacing data from 0–250  degreesC
T_dsc = np.arange(0, 251, 1)          # temperature [ degreesC]

# Baseline (constant ~0)
baseline = np.zeros_like(T_dsc)

# Glass transition of PLGA – a small step at 32  degreesC
Tg_plga = 32           #  degreesC
step_plga = 0.002      # mW min^-1 g^-1
gl_transition = np.where(T_dsc >= Tg_plga, step_plga, 0)

# Paracetamol melting – Gaussian peak centred at 169  degreesC
Tm_parac = 169
peak_std = 2           #  degreesC (half‑width 4  degreesC)
max_peak = 580         # mW min^-1 g^-1 (approx. heat of fusion x weight fraction)
parac_melt = max_peak * np.exp(-0.5 * ((T_dsc - Tm_parac) / peak_std)**2)

# Total heat flow
heat_flow = baseline + gl_transition + parac_melt

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758369582300/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
