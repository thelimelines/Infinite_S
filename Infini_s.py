import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from joblib import Parallel, delayed

def create_stussy_s_segments(bottom, top, depth):
    if depth == 0:
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

        size = np.linalg.norm(top - bottom)
        angle = (np.pi/2) + np.arctan2(top[1] - bottom[1], top[0] - bottom[0])

        rot_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

        segments = []

        for segment in norm_segments:
            new_segment = np.zeros_like(segment)
            for idx, point in enumerate(segment):
                scaled_point = point * size
                rotated_point = np.dot(rot_matrix, scaled_point)
                translated_point = rotated_point + (top + bottom)/2
                new_segment[idx] = translated_point
            segments.append(new_segment)

        return segments
    else:
        new_segments = []
        results = Parallel(n_jobs=-1)(delayed(create_stussy_s_segments)(segment[0], segment[-1], depth-1) for segment in create_stussy_s_segments(bottom, top, 0))
        for result in results:
            new_segments.extend(result)
        return new_segments

def create_fractal_segments(bottom, top, depth):
    segments = create_stussy_s_segments(bottom, top, depth)

    flat_segments = []
    for sublist in segments:
        for item in sublist:
            flat_segments.append(item)

    return flat_segments

depth = 3
draw_speed = float('inf')  # Maximum speed
segment_delay = 0  # No delay

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')

top = np.array([0, 2])
bottom = np.array([0, -2])

segments = create_stussy_s_segments(top, bottom, depth)

lines = [ax.plot([], [], lw=2, color='white')[0] for _ in segments]

def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    fig.tight_layout()
    for line in lines:
        line.set_data([], [])
    return lines

def animate(i):
    total_time = 0
    for j, segment in enumerate(segments):
        segment_len = np.sqrt(np.sum((segment[-1] - segment[0])**2))
        lines[j].set_data(segment[:, 0], segment[:, 1])
        total_time += segment_len / draw_speed
    return lines

frame_rate = 60
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(segments), interval=1000.0 / frame_rate, blit=True, repeat=False)

plt.show()