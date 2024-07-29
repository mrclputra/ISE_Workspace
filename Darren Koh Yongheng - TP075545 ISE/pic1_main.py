import matplotlib.pyplot as plt
import numpy as np
import os
from skimage import io, img_as_float

# Set window dimensions to 1080p (optional)
dpi = 100
width_inches = 1920 / dpi
height_inches = 1080 / dpi

# Get where image components are stored
components_dir = 'Assets\\Picture1'
png_files = [f for f in os.listdir(components_dir) if f.endswith('.png')]

# Here you can manually choose what files to load
# Array order dictates layer order
manual_order = ["Background_sky.png",
                "Foreground.png",
                "Traveller.png",
                "Shinning_Effect_Yellow_Orange.png",
                "Dust.png"]

# Ensure only files that exist in the directory are in the order
ordered_files = [file for file in manual_order if file in png_files]

# Load images in array based on manual order
images = []
for file in ordered_files:
    image_path = os.path.join(components_dir, file)
    image = img_as_float(io.imread(image_path))
    images.append(image)

# Plot images in specified order
plt.figure(1, figsize=(width_inches, height_inches), dpi=dpi)
plt.axis('off')

for image in images:
    plt.imshow(image)

# Save the combined image
output_path = 'Output\\combined_image.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

plt.show()
