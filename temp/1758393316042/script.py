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
import pandas as pd
import numpy as np

# Sample data (replace with your actual data)
x = np.linspace(0, 10, 20)  # Creates 20 evenly spaced numbers from 0 to 10
y = x**2 + 2*x + 1  # Example function: y = x^2 + 2x + 1


# --- Plotting the graph ---
plt.figure(figsize=(8, 6))  # Adjust figure size if needed

plt.plot(x, y, marker='o', linestyle='-', color='blue', label='y = x^2 + 2x + 1') # Plot the data
#  - marker:  'o' makes circles at each data point
#  - linestyle: '-' creates a solid line
#  - color: 'blue' sets the line color
#  - label: adds a label for the legend

plt.xlabel('X-axis')  # Label the x-axis
plt.ylabel('Y-axis')  # Label the y-axis
plt.title('Graph of Y vs X')  # Set the title of the plot
plt.grid(True)  # Add a grid for better readability
plt.legend()  # Show the legend (if you have labels)
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758393316042/plot.png', dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory  # Display the plot



# --- Creating a table ---

# Select 5 data points for the table
#  We use array slicing here to get a subset of the data
table_x = x[::len(x)//5][:5] #Take every len(x)/5 elements, up to the first 5. This keeps the array within bounds.
table_y = y[::len(y)//5][:5]

# Create a pandas DataFrame
data = {'X': table_x, 'Y': table_y}
df = pd.DataFrame(data)


# Print the table (or save it to a file)
print("\nTable of Data:")
print(df)

# Alternative: Save the table to a CSV file
# df.to_csv('data_table.csv', index=False)  # Saves the table to a file named "data_table.csv"
# print("\nTable saved to data_table.csv")


# --- Alternative table display (using matplotlib) ---

# If you prefer a visual table within the plot, you can use this:
fig, ax = plt.subplots(figsize=(8, 2))  # Create a new figure and axes

ax.axis('off')  # Turn off the axes
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center') #Create the table
table.auto_set_font_size(False)
table.set_fontsize(10) #Adjust font size.
table.scale(1.2,1.2) #adjust dimensions


plt.title("Data Table (Matplotlib)")
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758393316042/plot.png', dpi=150, bbox_inches='tight')
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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758393316042/data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_extract, f)
            
    print("Script executed successfully!")
except Exception as e:
    print(f"Note: Could not extract data - {e}")
