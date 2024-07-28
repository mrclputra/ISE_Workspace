import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from skimage import data

fig, ax = plt.subplots()
image = ax.imshow(data.coins(), cmap='gray')

def update(frame):
    # Update image data
    image.set_array(data.coins() * (1 + 0.1 * frame))
    return [image]

ani = FuncAnimation(fig, update, frames=10, blit=True)
plt.show()
