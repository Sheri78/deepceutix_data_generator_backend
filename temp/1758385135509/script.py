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

# --- Simple Line Plot Example ---

# Define data (x and y values)
x = np.array([1, 2, 3, 4, 5])  # Example x-values
y = np.array([2, 4, 1, 3, 5])  # Corresponding y-values

# Create the plot
plt.plot(x, y)  # Plot x versus y

# Add labels and title
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
plt.title("Simple Line Plot")

# Optionally, add a grid
plt.grid(True)

# Show the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory


# --- Scatter Plot Example ---

# Generate some random data for a scatter plot
np.random.seed(0)  # for reproducible results
x_scatter = np.random.rand(50)  # 50 random x-values between 0 and 1
y_scatter = np.random.rand(50)  # 50 random y-values between 0 and 1
colors = np.random.rand(50)  # Random colors for each point
sizes = (30 * np.random.rand(50))**2  # Random sizes for each point

# Create the scatter plot
plt.scatter(x_scatter, y_scatter, c=colors, s=sizes, alpha=0.5, cmap='viridis')

# Add labels and title
plt.xlabel("X-axis (Random)")
plt.ylabel("Y-axis (Random)")
plt.title("Scatter Plot Example")

# Add a colorbar to show the color mapping
plt.colorbar(label="Color Intensity")

# Show the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory



# --- Bar Chart Example ---

categories = ['Category A', 'Category B', 'Category C', 'Category D']
values = [25, 40, 15, 30]

plt.bar(categories, values)

# Add labels and title
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Bar Chart Example")

# Show the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory


# --- Histogram Example ---

# Generate some random data for a histogram
data = np.random.randn(1000)  # 1000 random values from a normal distribution

# Create the histogram
plt.hist(data, bins=30, color='skyblue', edgecolor='black')  # 30 bins

# Add labels and title
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.title("Histogram Example")

# Show the plot
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory

# --- Plotting multiple lines on the same plot ---

x = np.linspace(0, 10, 100)  # Create an array of 100 points between 0 and 10
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sine and Cosine Functions")
plt.legend()  # Show the legend
plt.grid(True)
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758385135509/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
