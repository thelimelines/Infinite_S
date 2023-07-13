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
    np.array([[0,-0.5],[-1,0.5]]),
    np.array([[-1,-0.5],[-0.5,0]]),
    np.array([[0.5,0],[1,0.5]])
]

# Define the drawing speed in units per second
draw_speed = 4.0

# Define the delay between segments in seconds
segment_delay = 0.1

fig, ax = plt.subplots()

def transform_segment(base, transform):
    scale, rotate, translate = transform
    # Apply the scale and rotation
    base = np.dot(base, np.array([[np.cos(rotate), -np.sin(rotate)], [np.sin(rotate), np.cos(rotate)]])) * scale
    # Apply the translation
    base += translate
    return base

def fractal_pattern(base, generations):
    if generations == 0:
        return base
    else:
        output = []
        for segment in base:
            # Define the transformations for this segment
            scale = np.sqrt(np.sum((segment[-1] - segment[0])**2))
            rotate = np.arctan2(segment[-1][1] - segment[0][1], segment[-1][0] - segment[0][0])
            translate = segment[0]
            # Apply the transformations to the base shape
            transformed = [transform_segment(seg, (scale, rotate, translate)) for seg in base]
            # Add the transformed shape to the output
            output.extend(transformed)
        # Recurse for the next generation
        return fractal_pattern(output, generations - 1)


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

# Define the base shape and number of generations
base = segments
generations = 3

# Generate the fractal pattern
segments = fractal_pattern(base, generations)

# Calculate total length of all segments
total_time = len(segments)

# Animation function
def animate(i):
    # Clear the current line data
    for line in lines:
        line.set_data([], [])
    # Draw the current segment
    if i < len(segments):
        lines[i % len(lines)].set_data(segments[i][:, 0], segments[i][:, 1])
    return lines

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=total_time, interval=1000.0/frame_rate, blit=True, repeat=False)

# Set the frame rate (frames per second)
frame_rate = 60

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=int((total_time + segment_delay) * frame_rate), interval=1000.0/frame_rate, blit=True, repeat=False)

plt.show()