import matplotlib.pyplot as plt
import numpy as np
import os
from skimage import io, exposure, img_as_float

# set window dimensions to 1080p (optional)
dpi = 100
width_inches = 1920 / dpi
height_inches = 1080 / dpi

# define where image components are stored
components_dir = 'marcel/components'
png_files = [f for f in os.listdir(components_dir) if f.endswith('.png')]

images = []
for file in png_files:
    image_path = os.path.join(components_dir, file)
    image = img_as_float(io.imread(image_path))
    images.append(image)

plt.figure(1, figsize=(width_inches, height_inches), dpi=dpi)
plt.axis('off')

for image in images:
    plt.imshow(image)

plt.show()