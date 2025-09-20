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

import pandas as pd
import numpy as np
import random
from datetime import datetime

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate synthetic data for 100 compounds
data = {
    'Compound_ID': [f'CID_{i:06d}' for i in range(1, 101)],
    'Molecular_Weight': np.random.uniform(50, 1000, 100).round(2),
    'LogP': np.random.normal(3, 1, 100),  # Logarithm of partition coefficient (octanol-water)
    'Hydrogen_Bond_Donors': np.random.randint(0, 5, 100),
    'Hydrogen_Bond_Acceptors': np.random.randint(0, 15, 100),
    'Topological_Polar_Surface_Area': np.random.uniform(0, 150, 100).round(1),
    'Molecular_Similarity': np.random.uniform(0, 1, 100).round(2),
    'Target_Receptor': np.random.choice(
        ['Muscarinic_Ach_R', 'Dopamine_D2', 'Serotonin_5HT2A', 'GABA_B', 'Beta_3_adrenergic'],
        100
    ),
    'IC50_values': np.random.uniform(0.01, 10, 100).round(3),
    'Lipinski_Violations': np.random.randint(0, 4, 100),
    'Classification': np.random.choice(['Lead', 'Hit', 'Active', 'Inactive'], 100),
    'Generated_Date': [datetime.now().strftime('%Y-%m-%d') for _ in range(100)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate derived features
df['Lipinski_Violations'] = (
    ((df['Molecular_Weight'] > 500) + 
     (df['Hydrogen_Bond_Donors'] > 5) + 
     (df['Hydrogen_Bond_Acceptors'] > 10) + 
     (df['Topological_Polar_Surface_Area'] > 140))
).astype(int)

df['Classification'] = np.where(
    df['IC50_values'] < 1.5,
    np.random.choice(['Active', 'Inactive'], 100),
    np.random.choice(['Hit', 'Lead'], 100)
)

# Display the first few rows
print(df.head())

# Save to CSV (optional)
df.to_csv('synthetic_pharmaceutical_data.csv', index=False)

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758372591518/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
