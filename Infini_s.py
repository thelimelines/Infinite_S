import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def create_stussy_s_segments(bottom, top, depth):
    if depth == 0:
        # Original 'Stussy S' segments centered at (0,0)
        norm_segments = [
            np.array([[-0.2, 0.1], [-0.2, 0.3]]), 
            np.array([[0, 0.1], [0, 0.3]]), 
            np.array([[0.2, 0.1], [0.2, 0.3]]), 
            np.array([[0.2, -0.1], [0.2, -0.3]]), 
            np.array([[0, -0.1], [0, -0.3]]), 
            np.array([[-0.2, -0.1], [-0.2, -0.3]]),
            np.array([[0,-0.1],[-0.2,0.1]]),
            np.array([[0.2,-0.1],[0,0.1]]),
            np.array([[-0.2, 0.3], [0, 0.5]]), 
            np.array([[0, 0.5], [0.2, 0.3]]), 
            np.array([[0.2,-0.3], [0, -0.5]]),
            np.array([[0, -0.5], [-0.2, -0.3]]),
            np.array([[-0.2,-0.1],[-0.1,0]]),
            np.array([[0.1,0],[0.2,0.1]])
        ]

        # Calculate the target size and angle
        size = np.linalg.norm(top - bottom)
        angle = (np.pi/2) + np.arctan2(top[1] - bottom[1], top[0] - bottom[0])

        # Create the rotation matrix
        rot_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

        # Initialize segments list
        segments = []

        # Scale, rotate, and translate each segment
        for segment in norm_segments:
            new_segment = np.zeros_like(segment)
            for idx, point in enumerate(segment):
                # Scale
                scaled_point = point * size
                # Rotate
                rotated_point = np.dot(rot_matrix, scaled_point)
                # Translate
                translated_point = rotated_point + (top + bottom)/2
                # Store new point
                new_segment[idx] = translated_point
            segments.append(new_segment)

        return segments
    else:
        new_segments = []
        for segment in create_stussy_s_segments(bottom, top, 0):
            new_segments += create_stussy_s_segments(segment[0], segment[-1], depth-1)
        return new_segments

def create_fractal_segments(bottom, top, depth):
    # Create the segments for the 'stussy s'
    segments = create_stussy_s_segments(bottom, top, depth)

    # Flatten the nested list of segments
    flat_segments = []
    for sublist in segments:
        for item in sublist:
            flat_segments.append(item)

    return flat_segments

depth=2

# Define the drawing speed in units per second
draw_speed = 10**depth

# Define the delay between segments in seconds
segment_delay = 10**-(depth+1)

fig, ax = plt.subplots()

# set the figure background to black
fig.patch.set_facecolor('black')

# Define the top and bottom points of the 'stussy s'
top = np.array([0, 2])
bottom = np.array([0, -2])

# Create the segments for the 'stussy s'
segments = create_stussy_s_segments(top, bottom, depth)

# Calculate total length of all segments (including delays)
total_time = sum(np.sqrt(np.sum(np.diff(segment, axis=0)**2, axis=1)).sum() / draw_speed + segment_delay for segment in segments)

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