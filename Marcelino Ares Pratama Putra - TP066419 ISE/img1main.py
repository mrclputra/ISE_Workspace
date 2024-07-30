import matplotlib.pyplot as plt
from skimage import io, img_as_float, exposure
from PIL import Image
import numpy as np
import os

# get where image components are stored
components_dir = 'Marcelino Ares Pratama Putra - TP066419 ISE/components'
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

def gamma(image, factor=1):
    modified_image = exposure.adjust_gamma(image, gamma=factor)
    return modified_image

# used for clouds, preserves alpha
def darken(image, gamma=1):
    # adjust the gamma value for darkening
    modified_image = exposure.adjust_gamma(image[:, :, :3], gamma)  # apply gamma correction to RGB channels

    # preserve alpha channel
    alpha_channel = image[:, :, 3]
    modified_image = np.dstack((modified_image, alpha_channel))  # reattach alpha channel

    return modified_image

def redden(image, intensity=1):
    if intensity < 0:
        raise ValueError("intensity must be a non-negative number")
    if image.shape[2] != 4:
        raise ValueError("input image must be an RGBA image")

    # copy image to modify
    modified_image = image.copy()

    # separate channels
    red_channel = modified_image[:, :, 0]
    green_channel = modified_image[:, :, 1]
    blue_channel = modified_image[:, :, 2]

    # apply red filter
    modified_image[:, :, 0] = np.clip(red_channel * intensity, 0, 1)

    # reduce other channels
    scale = max(0, 1 - 0.5 * (intensity - 1))   # this controls the amount of reduction
    modified_image[:, :, 1] = np.clip(green_channel * scale, 0, 1)
    modified_image[:, :, 2] = np.clip(blue_channel * scale, 0, 1)

    return modified_image

# modify images
modifications = {
    'time_traveller.png': [(redden, 1.2), (darken, 2)],
    'car_base.png': [(redden, 1.2), (darken, 2)],
    'base_ground.png': [(redden, 1.2), (darken, 3)],
    'fuji_base.png': [(redden, 1.5), (darken, 3)],
    'clouds_fuji.png': [(redden, 1.5), (darken, 5)],
    'clouds_sun.png': [(redden, 1.5), (darken, 5)],
    'clouds_close.png': [(redden, 1.5), (darken, 5)]
}

# apply modifications
for layer, funcs in modifications.items():
    if layer in layers:
        # Ensure funcs is a list of (function, arguments) tuples
        if not isinstance(funcs, list):
            funcs = [funcs]
        # Apply each function with its associated arguments
        for func, *args in funcs:
            layers[layer] = func(layers[layer], *args)

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

# comment / uncomment snippet below to save static frame 1 as an image
# combine images
for filename in manual_order:
        image = layers[filename]
        combined_image = overlayImage(combined_image, image)

pil_test_image = Image.fromarray((combined_image * 255).astype(np.uint8))
pil_test_image.save('Marcelino Ares Pratama Putra - TP066419 ISE/frame1.png')

# # create frames for increasing sun brightness
# frames = []
# for intensity in np.linspace(1, 1.5, 30):
#     # load and modify the images
#     combined_image = np.zeros_like(layers[manual_order[0]])

#     # apply filter to sun with increasing intensity
#     sun_image = layers['sun_red.png']

#     # scale the RGB channels by the brightness intensity factor
#     sun_image = np.clip(sun_image + (intensity - 1) * 0.12, 0, 1)

#     layers['sun_red.png'] = sun_image

#     # combine images
#     for filename in manual_order:
#         image = layers[filename]
#         combined_image = overlayImage(combined_image, image)

#     # linear brightness for final combines image
#     combined_image = np.clip(combined_image + (intensity - 1) * 0.7, 0, 1)
    
#     # convert to PIL Image and add to frames
#     pil_image = Image.fromarray((combined_image * 255).astype(np.uint8))
#     frames.append(pil_image)

# # Save the final GIF
# frames[0].save('Marcelino Ares Pratama Putra - TP066419 ISE/the_end_is_near.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
