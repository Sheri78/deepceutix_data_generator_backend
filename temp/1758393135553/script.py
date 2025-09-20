import numpy as np
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

import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Renders a simple HTML page with a placeholder for the chart."""
    return render_template('index.html')  # Create index.html in a 'templates' folder

@app.route('/data')
def get_data():
    """Returns the JSON data for the chart."""
    data = {
        "x": [4000, 3500, 3000, 2500, 2000, 1500, 1000, 500],
        "y": [0.1, 0.3, 0.2, 0.4, 0.8, 0.6, 0.3, 0.1]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


#index.html (place in a folder named "templates" next to your python file)

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758393135553/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
