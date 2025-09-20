import numpy as np
import matplotlib.pyplot as plt

# 1. Generate x values: 100 evenly spaced points from 0 to 2π
x = np.linspace(0, 2*np.pi, 100)  # or use np.arange(0, 2*np.pi, 0.01) for different spacing

# 2. Calculate y values (sine of x)
y = np.sin(x)

# 3. Create the plot
plt.plot(x, y)

# 4. Add labels and title (optional but recommended)
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.title("Sine Wave")

# 5. Add a grid (optional)
plt.grid(True)

# 6. Display the plot
plt.show()