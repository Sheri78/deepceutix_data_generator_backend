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
from faker import Faker
import random

# Initialize Faker
fake = Faker('en_US')

# Set seed for reproducibility
np.random.seed(42)

def generate_patients(n=100):
    """Generate patient demographic data."""
    return pd.DataFrame({
        'patient_id': [f'P-{i:04d}' for i in range(n)],
        'first_name': [fake.first_name() for _ in range(n)],
        'last_name': [fake.last_name() for _ in range(n)],
        'age': np.random.randint(18, 70, n),
        'gender': ['M' if random.random() > 0.5 else 'F' for _ in range(n)],
        'height': np.round(np.random.normal(165, 25, n)).astype(int),  # cm
        'weight': np.round(np.random.normal(70, 20, n)).astype(int),   # kg
        'diagnosis': [fake.medical_condition() for _ in range(n)],
        'insurance_provider': [fake.company() for _ in range(n)]
    })

def generate_drugs(n=20):
    """Generate drug catalog data."""
    drug_types = ['antibiotic', 'analgesic', 'antihypertensive', 'antidiabetic', 'antidepressant']
    drug_df = []
    for i in range(n):
        drug_id = f'DR-{i+1:03d}'
        drug_type = random.choice(drug_types)
        
        drug_df.append({
            'drug_id': drug_id,
            'name': fake.catch_phrase().replace('#', '').replace("'", ''),
            'generic_name': [''] + [fake.catch_phrase().replace('#', '').replace("'", '') for _ in range(5)][random.randint(0,5)],
            'dose_form': random.choice(['tablet', 'capsule', 'liquid', 'injection', 'suspension']),
            'strength': round(random.uniform(5, 500), 2),
            'route': random.choice(['oral', 'IV', 'topical', 'inhalation']),
            'therapeutic_class': drug_type,
            'indication': fake.medical_condition(),
            'contraindications': ', '.join(random.sample([fake.word() for _ in range(10)], k=random.randint(1,3)))
        })
    return pd.DataFrame(drug_df)

def generate_prescriptions(n=300):
    """Generate patient-drug prescription events with start and end dates."""
    start_dates = pd.date_range(start='2020-01-01', end='2023-01-01', freq='D').tolist()
    drug_ids = generate_drugs().drug_id.tolist()
    
    return pd.DataFrame({
        'prescription_id': [f'RX-{i:05d}' for i in range(n)],
        'patient_id': [f'P-{random.randint(0, 99):04d}' for _ in range(n)],
        'drug_id': [random.choice(drug_ids) for _ in range(n)],
        'start_date': [random.choice(start_dates) for _ in range(n)],
        'end_date': [random_date(start_dates[random.randint(0, len(start_dates)-1)]) for _ in range(n)],
        'dose_strength': np.random.randint(50, 300, n),
        'frequency': random.choice(['Daily', 'BID', 'TID', 'QID', 'Weekly']),
        'route': random.choice(['oral', 'IV', 'topical']),
        'doctor_provider': [fake.name() for _ in range(n)],
        'notes': [fake.sentence() for _ in range(n)]
    })

def generate_outcomes(n=300):
    """Generate clinical outcomes for prescriptions."""
    severity_levels = ['None', 'Mild', 'Moderate', 'Severe', 'Critical']
    
    return pd.DataFrame({
        'outcome_id': [f'OC-{i:05d}' for i in range(n)],
        'prescription_id': [f'RX-{random.randint(1, 299):05d}' for _ in range(n)],
        'adverse_event': [random.choice(['None', 'Headache', 'Nausea', 'Rash', 'Dizziness', 'None']) for _ in range(n)],
        'adverse_event_severity': [random.choice(severity_levels) for _ in range(n)],
        'efficacy': round(random.uniform(1.0, 5.0), 1),
        'visit_date': [random_date('2020-01-01', '2023-01-01') for _ in range(n)],
        'blood_pressure': f"{np.random.randint(80,180)}/{np.random.randint(40,120)} mmHg",
        'laboratory_value': f"{np.random.uniform(5.0, 20.0):.2f} mg/dL"
    })

# Helper function for date ranges
def random_date(start, end):
    """Generate a random date between start and end."""
    return pd.date_range(start=start, end=end, days=random.randint(0, 365)).random.choice()

# Generate datasets
patients = generate_patients()
drugs = generate_drugs()
prescriptions = generate_prescriptions()
outcomes = generate_outcomes()

# Sample the data (e.g., 10 rows) or save to CSV
print("Patient Data (Sample):")
print(patients.head())

# Save to CSV if needed
# patients.to_csv('synthetic_patients.csv', index=False)
# drugs.to_csv('synthetic_drugs.csv', index=False)
# prescriptions.to_csv('synthetic_prescriptions.csv', index=False)
# outcomes.to_csv('synthetic_outcomes.csv', index=False)

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758372537217/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
