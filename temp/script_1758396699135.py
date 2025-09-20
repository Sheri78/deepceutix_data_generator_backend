import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Plot of y vs x")
plt.grid(True)
plt.show()