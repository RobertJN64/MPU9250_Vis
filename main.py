import matplotlib.pyplot as plt

start = (0,0,0)
end = (5,5,-8)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2])
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])
plt.show()