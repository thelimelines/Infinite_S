import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Define the coordinates for the Super S as separate line segments
segments = [
    np.array([[-1, 0.5], [-1, 1.5]]), 
    np.array([[0, 0.5], [0, 1.5]]), 
    np.array([[1, 0.5], [1, 1.5]]), 
    np.array([[1, -0.5], [1, -1.5]]), 
    np.array([[0, -0.5], [0, -1.5]]), 
    np.array([[-1, -0.5], [-1, -1.5]]),
    np.array([[0,-0.5],[-1,0.5]]),
    np.array([[1,-0.5],[0,0.5]]),
    np.array([[-1, 1.5], [0, 2.5]]), 
    np.array([[0, 2.5], [1, 1.5]]), 
    np.array([[1,-1.5], [0, -2.5]]),
    np.array([[0, -2.5], [-1, -1.5]]),
    np.array([[-1,-0.5],[-0.5,0]]),
    np.array([[0.5,0],[1,0.5]])
]

# Define the drawing speed in units per second
draw_speed = 4.0

# Define the delay between segments in seconds
segment_delay = 0.1

fig, ax = plt.subplots()

# set the figure background to black
fig.patch.set_facecolor('black')

# Creating empty line objects
lines = [ax.plot([], [], lw=2, color='white')[0] for _ in segments]

# Initialization function
def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    fig.tight_layout()
    for line in lines:
        line.set_data([], [])
    return lines

# Calculate total length of all segments (including delays)
total_time = sum(np.sqrt(np.sum(np.diff(segment, axis=0)**2, axis=1)).sum() / draw_speed + segment_delay for segment in segments)

# Animation function
def animate(i):
    time = i * (1.0/60.0)  # convert frame number to time
    total_time = 0
    for j, segment in enumerate(segments):
        segment_len = np.sqrt(np.sum((segment[-1] - segment[0])**2))
        segment_time = segment_len / draw_speed
        if total_time <= time < total_time + segment_time:
            t = (time - total_time) / segment_time
            point = segment[0] + t * (segment[-1] - segment[0])
            lines[j].set_data(*zip(segment[0], point))
            return lines
        elif total_time <= time < total_time + segment_time + segment_delay:
            lines[j].set_data(segment[:, 0], segment[:, 1])
            return lines
        lines[j].set_data(segment[:, 0], segment[:, 1])
        total_time += segment_time + segment_delay
    return lines

# Set the frame rate (frames per second)
frame_rate = 60

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=int((total_time + segment_delay) * frame_rate), interval=1000.0/frame_rate, blit=True, repeat=False)

plt.show()