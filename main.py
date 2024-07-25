import matplotlib.pyplot as plt
import numpy as np
from skimage import io, exposure, img_as_float

img1 = img_as_float(io.imread('components/background_base.png'))

plt.figure(1)
plt.imshow(img1)

plt.show()