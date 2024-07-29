import matplotlib.pyplot as plt
from skimage import io, img_as_float, exposure, restoration, transform
from skimage.color import rgb2hsv, hsv2rgb
from PIL import Image # for gif
import numpy as np
import os

# get image folder
components_dir = 'Marcelino Ares Pratama Putra - TP066419 ISE/components2'
png_files = [f for f in os.listdir(components_dir) if f.endswith('.png')]

# define layer order here
manual_order = [
    'space.png',
    'sun.png',
    'clouds.png',
    'earth.png',
    'moon.png',
    'flag_shadow.png',
    'flag.png'
]

# load images into a dictionary
layers = {}
for filename in manual_order:
    filepath = os.path.join(components_dir, filename)
    image = img_as_float(io.imread(filepath))
    layers[filename] = image

# do image modifications here

def denoise(image, intensity = 1):
    if intensity < 0:
        raise ValueError("intensity must be a non-negative number")
    if image.shape[2] != 4:
        raise ValueError("input image must be an RGBA image")
    
    rgb_image = image[:, :, :3]
    alpha_channel = image[:, :, 3]

    # apply denoising to rgb channels
    rgb_image = restoration.denoise_tv_chambolle(rgb_image, weight=intensity)

    # recombine with alpha
    modified_image = np.dstack((rgb_image, alpha_channel))

    return modified_image

def saturate(image, factor=1):
    if factor < 0:
        raise ValueError("intensity must be a non-negative number")
    if image.shape[2] != 4:
        raise ValueError("input image must be an RGBA image")
    
    # separate channels
    rgba = image[..., :3]
    alpha = image[..., 3]

    # convert rgb to hsv
    hsv = rgb2hsv(rgba)
    hsv[..., 1] *= factor

    # clip to 0-1 range
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 1)

    # convert back
    rgb = hsv2rgb(hsv)

    # recombine with alpha
    modified_image = np.dstack((rgb, alpha))

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

# adjust earth gamma levels, emulate shadow pointing camera
mod_layer = layers['earth.png']
mod_layer = exposure.adjust_gamma(mod_layer, gamma=2)
layers['earth.png'] = mod_layer

# modify flag
mod_layer = layers['flag.png']
mod_layer = exposure.adjust_gamma(mod_layer, gamma=2)
layers['flag.png'] = mod_layer

# handle function modifications
modifications = {
    'earth.png': [(redden, 1.2)],
    'moon.png': [(redden, 1.4)],
    'flag.png': [(denoise, 0.2), (saturate, 0.4), (redden, 1.4)],
    'clouds.png': [(redden, 4)]
}

# apply modifications
for layer, funcs in modifications.items():
    if layer in layers:
        # Ensure funcs is a list of (function, argument) tuples
        if not isinstance(funcs, list):
            funcs = [funcs]
        # Apply each function with its associated argument
        for func, arg in funcs:
            layers[layer] = func(layers[layer], arg)

# initialize final image dimensions
image_height, image_width, image_depth = layers[manual_order[0]].shape
# create transparent canvas
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

# gif frames
frames = []
num_frames = 60
frequency = 0.05 # how fast it should flash
earth_movement = 0.07

# move earth left first
layers['earth.png'] = transform.warp(layers['earth.png'], transform.AffineTransform(translation=(-120, 0)).inverse, mode='edge', preserve_range=True)

for i in range(num_frames):
    # base image for each frame
    combined_image = np.zeros_like(layers[manual_order[0]])

    # calculate sun intensity with a sine wave
    intensity = 1 + 0.1 * np.sin(2 * np.pi * frequency * i)

    # load and modify sun
    sun_image = layers['sun.png']
    sun_image = np.clip(sun_image + (intensity - 1) * 0.12, 0, 1)
    layers['sun.png'] = sun_image

    # move earth towards the right
    earth_image = layers['earth.png']
    image_height, image_width, _ = earth_image.shape
    x_shift = i * earth_movement  # pixels to move the earth image

    # translation matrix
    translation_matrix = transform.AffineTransform(translation=(x_shift, 0))
    earth_transformed = transform.warp(earth_image, translation_matrix.inverse, mode='edge', preserve_range=True)

    layers['earth.png'] = earth_transformed

    # Combine images
    for filename in manual_order:
        image = layers[filename]
        combined_image = overlayImage(combined_image, image)

    # Convert to PIL image and add to frames
    pil_image = Image.fromarray((combined_image * 255).astype(np.uint8))
    frames.append(pil_image)

frames[0].save('Marcelino Ares Pratama Putra - TP066419 ISE/img2_moonview.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)