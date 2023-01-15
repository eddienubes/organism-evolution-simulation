from matplotlib import pyplot as plt

x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y = [1.9, 7.44, 14.025, 10.9, 13.7, 19.95, 21.85, 13.57, 27.86, 41.6]
velocity_y = [0.4, 0.65, 0.73, 0.77, 0.765, 0.755, 0.64, 0.62, 0.61, 0.60]


# plt.plot(x, y)
plt.plot(x, velocity_y)
plt.title('Velocity')
plt.xlabel('Amount of food')
plt.ylabel('Velocity AVG')
plt.show()