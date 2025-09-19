import matplotlib.pyplot as plt
import numpy as np

# Release Data (from JSON)
time = [0, 1, 2, 4, 6, 8, 10, 12]
release = [0, 15, 28, 45, 62, 75, 85, 92]

# Calculate Release Rate (optional - already in the table, but good for visualization)
release_rate = np.diff(release) / np.diff(time)

# Create the Plot
plt.figure(figsize=(10, 6))  # Adjust figure size for better readability

plt.plot(time, release, marker='o', linestyle='-', color='blue', label='Cumulative Release')
plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Cumulative Drug Release (%)', fontsize=12)
plt.title('Dissolution Profile of Sustained-Release Tablet', fontsize=14)

# Add Release Rate (Optional - as secondary y-axis)
ax2 = plt.gca().twinx()
ax2.plot(time[1:], release_rate, marker='x', linestyle='--', color='red', label='Release Rate (%/hour)')
ax2.set_ylabel('Release Rate (%/hour)', fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')


plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 12.5) # Set x axis limits to show all data and have a buffer
plt.ylim(0,100)
plt.legend(loc='upper left')

# Add a second legend for the release rate
lines, labels = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines + lines2, labels + labels2, loc='upper left')


plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758196842068/plot.png', dpi=150, bbox_inches='tight')

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758196842068/data.json', 'w') as f:
            json.dump(data_to_extract, f)
except Exception as e:
    print(f"Could not extract data: {e}")
