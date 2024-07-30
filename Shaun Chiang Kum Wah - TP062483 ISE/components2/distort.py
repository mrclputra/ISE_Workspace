import cv2
import numpy as np
from PIL import Image, ImageDraw
import random

# Function to load an image and convert it to RGBA
def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 3:  # If the image doesn't have an alpha channel
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    return Image.fromarray(image)

# Function to resize images to match the size of the base image
def resize_to_match(base_image, image_to_resize):
    return image_to_resize.resize(base_image.size, Image.LANCZOS)

# Load your layers
layer1 = load_image('Shaun Chiang Kum Wah - TP062483 ISE/components2/dark.png')
# layer2 = load_image('path_to_your_image/layer2.png')
layer3 = load_image('Shaun Chiang Kum Wah - TP062483 ISE/components2/arcdetriomphe_bg.png')  # The layer to apply the glitch effect

# Ensure all layers are the same size
# layer2 = resize_to_match(layer1, layer2)
layer3 = resize_to_match(layer1, layer3)

# Function to create a glitch frame
def create_glitch_frame(image, intensity=5):
    width, height = image.size
    glitched_image = image.copy()
    
    for _ in range(intensity):
        x_start = random.randint(0, width - 50)
        y_start = random.randint(0, height - 50)
        x_end = random.randint(x_start + 1, min(x_start + 50, width))
        y_end = random.randint(y_start + 1, min(y_start + 50, height))
        
        box = (x_start, y_start, x_end, y_end)
        region = glitched_image.crop(box)
        
        x_offset = random.randint(-30, 30)  # Increase offset range
        y_offset = random.randint(-30, 30)  # Increase offset range
        glitched_image.paste(region, (x_start + x_offset, y_start + y_offset))
    
    return glitched_image

# Create frames for the GIF
frames = []
for i in range(1, 10):
    # Apply the glitch effect to layer3
    glitched_layer = create_glitch_frame(layer3, intensity=i * 10)  # Increase intensity progressively
    
    # Combine layers
    # combined = Image.alpha_composite(layer1.convert("RGBA"), layer2.convert("RGBA"))
    combined = Image.alpha_composite(layer1.convert("RGBA"), glitched_layer.convert("RGBA"))
    
    frames.append(combined)

# Save the frames as a GIF
gif_path = 'Shaun Chiang Kum Wah - TP062483 ISE/what_has_happened.gif'
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0)

