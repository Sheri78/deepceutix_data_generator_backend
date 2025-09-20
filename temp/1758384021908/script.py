import numpy as np
# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from tabulate import tabulate  # pip install tabulate

# Load the JSON data
json_data = """
{
  "chart": {
    "type": "line",
    "data": {
      "labels": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      "datasets": [
        {
          "label": "Website Visits",
          "data": [1200, 1500, 1300, 1800, 2000, 1000, 800],
          "borderColor": "rgb(75, 192, 192)",
          "tension": 0.1
        }
      ]
    },
    "options": {
      "scales": {
        "y": {
          "beginAtZero": true,
          "title": {
            "display": true,
            "text": "Number of Visits"
          }
        },
        "x": {
          "title": {
            "display": true,
            "text": "Day of the Week"
          }
        }
      },
      "plugins": {
        "title": {
          "display": true,
          "text": "Weekly Website Traffic",
          "padding": 10,
          "font": {
            "size": 16
          }
        }
      }
    }
  },
  "table": {
    "columns": ["Day", "Visits", "Bounce Rate (%)", "Avg. Session Duration (s)"],
    "rows": [
      {"Day": "Monday", "Visits": 1200, "Bounce Rate (%)": 35, "Avg. Session Duration (s)": 120},
      {"Day": "Tuesday", "Visits": 1500, "Bounce Rate (%)": 30, "Avg. Session Duration (s)": 150},
      {"Day": "Wednesday", "Visits": 1300, "Bounce Rate (%)": 40, "Avg. Session Duration (s)": 130},
      {"Day": "Thursday", "Visits": 1800, "Bounce Rate (%)": 25, "Avg. Session Duration (s)": 160},
      {"Day": "Friday", "Visits": 2000, "Bounce Rate (%)": 20, "Avg. Session Duration (s)": 180},
      {"Day": "Saturday", "Visits": 1000, "Bounce Rate (%)": 50, "Avg. Session Duration (s)": 90},
      {"Day": "Sunday", "Visits": 800, "Bounce Rate (%)": 55, "Avg. Session Duration (s)": 80}
    ]
  }
}
"""  # Paste the full JSON content here, either as a string or from a file

data = json.loads(json_data)

# Plot the graph (using Matplotlib)
chart_data = data['chart']['data']
labels = chart_data['labels']
visits = chart_data['datasets'][0]['data'] # Assumes only one dataset
plt.figure(figsize=(10, 6))  # Adjust size as needed
plt.plot(labels, visits, marker='o', linestyle='-', color='rgb(75, 192, 192)')
plt.title(data['chart']['options']['plugins']['title']['text'])
plt.xlabel(data['chart']['options']['scales']['x']['title']['text'])
plt.ylabel(data['chart']['options']['scales']['y']['title']['text'])
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758384021908/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

# Create the table (using tabulate)
table_data = data['table']['rows']
table_headers = data['table']['columns']

# Extract data for tabulate in the correct order
table_values = []
for row in table_data:
  table_values.append([row[col] for col in table_headers])

print(tabulate(table_values, headers=table_headers, tablefmt="grid")) #  Try "pipe", "simple", "github" for different styles.

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758384021908/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
