import matplotlib.pyplot as plt
import random

# Generate some random data for c and d
c = [random.uniform(0, 10) for _ in range(5)]  # 5 random numbers between 0 and 10
d = [random.uniform(0, 10) for _ in range(5)]  # 5 random numbers between 0 and 10


# Create the plot
plt.plot(c, d, marker='o', linestyle='-', color='blue')  # You can customize marker, line, color

# Add labels and title
plt.xlabel("c")
plt.ylabel("d")
plt.title("Graph of c vs. d")

# Add grid lines (optional)
plt.grid(True)

# Show the plot
plt.show()