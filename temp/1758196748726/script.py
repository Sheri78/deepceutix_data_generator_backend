import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import trapz

# Define PK parameters
ka = 1.0  # Absorption rate constant (1/h) - Quick absorption
ke = np.log(2) / 6  # Elimination rate constant (1/h), derived from half-life = 6 hours
dose = 100  # Dose in mg (Arbitrary for demonstration)
Vd = 2  # Volume of distribution in L (Arbitrary for demonstration)

# Time points
time = np.linspace(0, 24, 25)  # 25 time points from 0 to 24 hours

# Function to calculate concentration at a given time using a one-compartment model
def calculate_concentration(t, ka, ke, dose, Vd):
    """Calculates the plasma concentration at time t.

    Args:
        t: Time in hours.
        ka: Absorption rate constant (1/h).
        ke: Elimination rate constant (1/h).
        dose: Dose in mg.
        Vd: Volume of distribution in L.

    Returns:
        Plasma concentration in mg/L.
    """
    concentration = (dose * ka / Vd) * (np.exp(-ke * t) - np.exp(-ka * t)) / (ka - ke)
    return concentration

# Calculate concentrations
concentrations = [calculate_concentration(t, ka, ke, dose, Vd) for t in time]

# Add a small amount of noise to simulate real-world data
noise = np.random.normal(0, 0.5, len(concentrations))  # Mean 0, SD 0.5
concentrations = [max(0, c + n) for c, n in zip(concentrations, noise)] #ensure no negative values


# Find Cmax and Tmax
Cmax = max(concentrations)
Tmax = time[concentrations.index(Cmax)]

# Calculate AUC using the trapezoidal rule
AUC = trapz(concentrations, time)

# Calculate half-life using two points after Cmax (for demonstration in the markdown table)
time_for_halflife = time[time > Tmax]
concentration_for_halflife = [c for t, c in zip(time, concentrations) if t > Tmax]

# Ensure that there are at least 2 points after Tmax to perform a half-life calculation
if len(concentration_for_halflife) >= 2:
    # Pick the first two points after Tmax
    c1 = concentration_for_halflife[0]
    c2 = concentration_for_halflife[1]
    t1 = time_for_halflife[0]
    t2 = time_for_halflife[1]

    # Calculate half-life
    halflife_calculated = (t2 - t1) * np.log(2) / np.log(c1/c2)
else:
    halflife_calculated = "Insufficient data after Tmax"


# 1. JSON Data
data = {"time": time.tolist(), "concentration": concentrations}
json_data = json.dumps(data, indent=4)
print("JSON Data:\n", json_data)


# 2. Markdown Table
df = pd.DataFrame({"Time (h)": time, "Concentration (mg/L)": concentrations})

# Create a column with the Half-life calculation results
if halflife_calculated != "Insufficient data after Tmax":
    df["Half-life Calculation (h)"] = ["N/A"] * df.shape[0]
    df.at[0, "Half-life Calculation (h)"] = f"Using points {time_for_halflife[0]:.2f}h, {time_for_halflife[1]:.2f}h : {halflife_calculated:.2f}"
else:
    df["Half-life Calculation (h)"] = ["N/A"] * df.shape[0]
    df.at[0, "Half-life Calculation (h)"] = "Insufficient data after Tmax"

markdown_table = df.to_markdown(index=False, floatfmt=".2f")
print("\nMarkdown Table:\n", markdown_table)


# 3. Python Code (Matplotlib Plot)
plt.figure(figsize=(10, 6))
plt.semilogy(time, concentrations, marker='o', linestyle='-')
plt.xlabel("Time (hours)")
plt.ylabel("Concentration (mg/L) - Log Scale")
plt.title("Plasma Concentration vs. Time (Semi-Log Scale)")
plt.grid(True)
plt.savefig('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758196748726/plot.png', dpi=150, bbox_inches='tight')


# 4. PK Parameters
print("\nPK Parameters:")
print(f"Cmax: {Cmax:.2f} mg/L")
print(f"Tmax: {Tmax:.2f} hours")
print(f"AUC: {AUC:.2f} mg*h/L")

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
        with open('C:/Users/DELL/Desktop/deepceutix/backend/deepceutix_data-generator_backend/temp/1758196748726/data.json', 'w') as f:
            json.dump(data_to_extract, f)
except Exception as e:
    print(f"Could not extract data: {e}")
