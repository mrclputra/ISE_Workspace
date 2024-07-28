import matplotlib.pyplot as plt
import numpy as np
import os
from skimage import io, img_as_float, color, filters

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
    'sun_red.png',
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

def applyRedFilter(image, intensity=1):
    if intensity < 0:
        raise ValueError("intensity factor must be a non-negative value.")
    if image.shape[2] != 4:
        raise ValueError("input image must be an RGBA image.")
    
    # copy image to modify
    modified_image = image.copy()

    # adjust the red channel and keep green and blue channels low
    red_channel = modified_image[:, :, 0]
    green_channel = modified_image[:, :, 1]
    blue_channel = modified_image[:, :, 2]

    # Apply red filter
    modified_image[:, :, 0] = np.clip(red_channel * intensity, 0, 1)
    
    # Scale green and blue channels
    scale = max(0, 1 - 0.9 * (intensity - 1))
    modified_image[:, :, 1] = np.clip(green_channel * scale, 0, 1)
    modified_image[:, :, 2] = np.clip(blue_channel * scale, 0, 1)

    return modified_image

# modify ground
layer_to_modify = 'base_ground.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

# modify person
layer_to_modify = 'time_traveller.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

# modify fuji
layer_to_modify = 'fuji_base.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

# modify clouds
layer_to_modify = 'clouds_fuji.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

layer_to_modify = 'clouds_sun.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

layer_to_modify = 'clouds_close.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

# car
layer_to_modify = 'car_base.png'
if layer_to_modify in layers:
    layers[layer_to_modify] = applyRedFilter(layers[layer_to_modify], 1.5)

# initialize dimensions
image_height, image_width, image_depth = layers[manual_order[0]].shape
# initialize a transparent canvas
combined_image = np.zeros((image_height, image_width, 4), dtype=np.float32)

# function to overlay transparent png images
def overlayImage(base, overlay):
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

# combine images in specified
for filename in manual_order:
    image = layers[filename]
    combined_image = overlayImage(combined_image, image)

# plt.imshow(layers['car_base.png'])

# Display the result
plt.figure(figsize=(15, 15))
plt.imshow(combined_image)
plt.axis('off')  # Hide axes
plt.tight_layout()
plt.show()
