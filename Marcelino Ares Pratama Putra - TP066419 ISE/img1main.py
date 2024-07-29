import matplotlib.pyplot as plt
from skimage import io, img_as_float
from skimage.exposure import adjust_gamma
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

def darken(image, gamma=1):
    if gamma < 0:
        raise ValueError("Gamma factor must be a non-negative value.")
    if image.shape[2] != 4:
        raise ValueError("Input image must be an RGBA image.")
    
    # adjust the gamma value for darkening
    modified_image = adjust_gamma(image[:, :, :3], gamma)  # apply gamma correction to RGB channels

    # preserve alpha channel
    alpha_channel = image[:, :, 3]
    modified_image = np.dstack((modified_image, alpha_channel))  # reattach alpha channel

    return modified_image

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

    # apply red filter
    modified_image[:, :, 0] = np.clip(red_channel * intensity, 0, 1)
    
    # scale green and blue channels
    scale = max(0, 1 - 0.5 * (intensity - 1))
    modified_image[:, :, 1] = np.clip(green_channel * scale, 0, 1)
    modified_image[:, :, 2] = np.clip(blue_channel * scale, 0, 1)

    return modified_image

# modify images
modifications = {
    'time_traveller.png': [(applyRedFilter, 1.2), (darken, 2)],
    'car_base.png': [(applyRedFilter, 1.2), (darken, 2)],
    'base_ground.png': [(applyRedFilter, 1.2), (darken, 3)],
    'fuji_base.png': [(applyRedFilter, 1.5), (darken, 3)],
    'clouds_fuji.png': [(applyRedFilter, 1.5), (darken, 5)],
    'clouds_sun.png': [(applyRedFilter, 1.5), (darken, 5)],
    'clouds_close.png': [(applyRedFilter, 1.5), (darken, 5)]
}

# apply modifications
for layer, funcs in modifications.items():
    if layer in layers:
        if isinstance(funcs, list):
            func, arg = funcs
            layers[layer] = func(layers[layer], arg)
        else:
            for func, arg in funcs:
                layers[layer] = func(layers[layer], arg)

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

# create frames for increasing sun brightness
frames = []
for intensity in np.linspace(1, 1.5, 30):
    # load and modify the images
    combined_image = np.zeros_like(layers[manual_order[0]])

    # apply filter to sun with increasing intensity
    sun_image = layers['sun_red.png']

    # scale the RGB channels by the brightness intensity factor
    sun_image = np.clip(sun_image + (intensity - 1) * 0.12, 0, 1)

    layers['sun_red.png'] = sun_image

    # combine images
    for filename in manual_order:
        image = layers[filename]
        combined_image = overlayImage(combined_image, image)

    # linear brightness for final combines image
    combined_image = np.clip(combined_image + (intensity - 1) * 0.7, 0, 1)
    
    # convert to PIL Image and add to frames
    pil_image = Image.fromarray((combined_image * 255).astype(np.uint8))
    frames.append(pil_image)

# Save the final GIF
frames[0].save('Marcelino Ares Pratama Putra - TP066419 ISE/the_end_is_near.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
