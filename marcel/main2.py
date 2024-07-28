import matplotlib.pyplot as plt
import numpy as np
import os
from skimage import io, img_as_float

# set window dimensions to 1080p (optional)
dpi = 100
width_inches = 1920 / dpi
height_inches = 1080 / dpi

# get where image components are stored
components_dir = 'marcel/components'
png_files = [f for f in os.listdir(components_dir) if f.endswith('.png')]

# define layer order here
manual_order = [
    'base_sky.png',
    'sun_redgiant.png',
    'clouds_sun.png',
    'fuji_base.png',
    'base_ground.png',
    'clouds_fuji.png',
    'clouds_close.png',
    'car_base.png',
    'subject_shadows.png',
    'time_traveller.png'
]

# load images into a dictionary
layers = {}
for filename in manual_order:
    filepath = os.path.join(components_dir, filename)
    image = img_as_float(io.imread(filepath))
    layers[filename] = image

image_height, image_width, image_depth = layers[manual_order[0]].shape

# Initialize a transparent canvas
combined_image = np.zeros((image_height, image_width, 4), dtype=np.float32)

# Function to overlay images
def overlay_image(base, overlay):
    x, y = 0, 0  # Change coordinates if needed for positioning
    overlay_height, overlay_width, _ = overlay.shape
    template = np.zeros((base.shape[0], base.shape[1], 4), dtype=np.float32)
    template[y:y+overlay_height, x:x+overlay_width, :] = overlay
    
    mask = template[:, :, 3]
    inv_mask = 1. - mask
    result = base[:, :, :3] * inv_mask[:, :, np.newaxis] + template[:, :, :3] * mask[:, :, np.newaxis]
    base[:, :, :3] = result
    base[:, :, 3] = inv_mask + mask
    return base

# Combine images in the specified order
for filename in manual_order:
    image = layers[filename]
    combined_image = overlay_image(combined_image, image)

# Display the result
plt.figure(figsize=(15, 15))
plt.subplot(1, 1, 1)
plt.imshow(combined_image)
plt.axis('off')  # Hide axes
plt.tight_layout()
plt.show()