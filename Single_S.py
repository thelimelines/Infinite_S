import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Define the coordinates for the Super S as separate line segments
segments = [np.array([[-1, 0.5], [-1, 1.5]]), 
            np.array([[0, 0.5], [0, 1.5]]), 
            np.array([[1, 0.5], [1, 1.5]]), 
            np.array([[1, -0.5], [1, -1.5]]), 
            np.array([[0, -0.5], [0, -1.5]]), 
            np.array([[-1, -0.5], [-1, -1.5]]),
            np.array([[0,-0.5],[-1,0.5]]),
            np.array([[1,-0.5],[0,0.5]]),
            np.array([[-1, 1.5], [0, 2.5], [1, 1.5]]), 
            np.array([[1,-1.5], [0, -2.5], [-1, -1.5]]),
            np.array([[0,-0.5],[-1,0.5]]),
            np.array([[-1,-0.5],[-0.5,0]]),
            np.array([[0.5,0],[1,0.5]])]

fig, ax = plt.subplots()

# Creating empty line objects
lines = [ax.plot([], [], lw=2)[0] for _ in range(len(segments))]

# Initialization function
def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-3, 3)
    for line in lines:
        line.set_data([], [])
    return lines

# Animation function
def animate(i):
    for j in range(min(i+1, len(segments))):
        lines[j].set_data(segments[j][:, 0], segments[j][:, 1])
    return lines

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(segments), interval=2000/len(segments), blit=True)

# Remove the axes
plt.axis('off')
plt.show()