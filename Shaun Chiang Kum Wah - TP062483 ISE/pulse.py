from PIL import Image, ImageEnhance
import numpy as np
import math

def create_pulsating_gif(input_image_path, output_gif_path, frames=60, gif_duration=100, max_brightness=2.0):
    # Load the image
    original_image = Image.open(input_image_path).convert('RGB')
    
    # List to hold the frames for the GIF
    pulse_frames = []

    # Generate frames with pulsating intensity
    for i in range(frames):
        # Calculate the pulse factor (from neutral to high)
        pulse_factor = (math.sin(2 * math.pi * i / frames) + 1) / 2  # Sinusoidal wave between 0 and 1
        
        # Adjust the image brightness
        enhancer = ImageEnhance.Brightness(original_image)
        pulsed_image = enhancer.enhance(1 + pulse_factor * (max_brightness - 1))  # Neutral (1) to High (max_brightness)
        
        # Add the pulsed image to the frames list
        pulse_frames.append(pulsed_image)
    
    # Save the frames as a GIF
    pulse_frames[0].save(
        output_gif_path, 
        save_all=True, 
        append_images=pulse_frames[1:], 
        duration=gif_duration, 
        loop=0
    )

    print(f"Pulsating GIF saved as {output_gif_path}")

# Example usage
input_image_path = 'Shaun Chiang Kum Wah - TP062483 ISE/components/overlayed.png'  # Path to your input image
output_gif_path = 'Shaun Chiang Kum Wah - TP062483 ISE/something_is_off.gif'  # Path where the output GIF will be saved

# Adjust these parameters to control the pulsation effect
frames = 80  # Number of frames in the GIF
gif_duration = 40  # Duration of each frame in milliseconds
max_brightness = 1.5  # Maximum brightness factor (2.0 means double the brightness)

create_pulsating_gif(input_image_path, output_gif_path, frames, gif_duration, max_brightness)
