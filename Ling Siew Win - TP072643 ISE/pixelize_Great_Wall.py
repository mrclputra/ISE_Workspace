from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from rembg import remove

def enhance_color(image, enhancement_factor):
    # Enhance the color of the image
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(enhancement_factor)

def plot_color_histograms(original_image, enhanced_image):
    # Convert images to numpy arrays
    original_np = np.array(original_image)
    enhanced_np = np.array(enhanced_image)
    
    # Flatten the image arrays and separate color channels
    r_orig, g_orig, b_orig = original_np[..., 0].flatten(), original_np[..., 1].flatten(), original_np[..., 2].flatten()
    r_enh, g_enh, b_enh = enhanced_np[..., 0].flatten(), enhanced_np[..., 1].flatten(), enhanced_np[..., 2].flatten()
    
    # Plot histograms for each channel
    plt.figure(figsize=(14, 10))
    
    # Original Image Histograms
    plt.subplot(2, 3, 1)
    plt.hist(r_orig, bins=256, color='red', alpha=0.6)
    plt.title('Original Red Channel')
    
    plt.subplot(2, 3, 2)
    plt.hist(g_orig, bins=256, color='green', alpha=0.6)
    plt.title('Original Green Channel')
    
    plt.subplot(2, 3, 3)
    plt.hist(b_orig, bins=256, color='blue', alpha=0.6)
    plt.title('Original Blue Channel')
    
    # Enhanced Image Histograms
    plt.subplot(2, 3, 4)
    plt.hist(r_enh, bins=256, color='red', alpha=0.6)
    plt.title('Enhanced Red Channel')
    
    plt.subplot(2, 3, 5)
    plt.hist(g_enh, bins=256, color='green', alpha=0.6)
    plt.title('Enhanced Green Channel')
    
    plt.subplot(2, 3, 6)
    plt.hist(b_enh, bins=256, color='blue', alpha=0.6)
    plt.title('Enhanced Blue Channel')
    
    plt.tight_layout()

def pixelize_and_display_images(input_image_path, dragon_image_path, traveller_image_path, pixel_size, color_enhancement_factor, dragon_resize_factor, traveller_resize_factor):
    # Open the original image
    original_image = Image.open(input_image_path)
    
    # Enhance the color of the original image
    enhanced_image = enhance_color(original_image, color_enhancement_factor)
    
    # Pixelize the enhanced image
    pixelized_image = enhanced_image.resize(
        (enhanced_image.width // pixel_size, enhanced_image.height // pixel_size),
        resample=Image.Resampling.NEAREST
    )
    pixelized_image = pixelized_image.resize(
        (pixelized_image.width * pixel_size, pixelized_image.height * pixel_size),
        resample=Image.Resampling.NEAREST
    )

    # Remove the background from the dragon image
    dragon_image = Image.open(dragon_image_path).convert("RGBA")
    dragon_no_bg = remove(dragon_image)

    # Resize the dragon image to be larger based on the resize factor
    dragon_size = (int(dragon_no_bg.width * dragon_resize_factor), int(dragon_no_bg.height * dragon_resize_factor))
    resized_dragon = dragon_no_bg.resize(dragon_size, Image.Resampling.LANCZOS)

    # Remove the background from the traveller image
    traveller_image = Image.open(traveller_image_path).convert("RGBA")
    traveller_no_bg = remove(traveller_image)

    # Save the background-removed traveller image as a PNG file
    traveller_no_bg.save('traveller_no_bg.png')
    
    # Resize the traveller image
    traveller_size = (int(traveller_no_bg.width * traveller_resize_factor), int(traveller_no_bg.height * traveller_resize_factor))
    resized_traveller = traveller_no_bg.resize(traveller_size, Image.Resampling.LANCZOS)

    # Pixelize the traveller image
    pixelized_traveller = resized_traveller.resize(
        (resized_traveller.width // pixel_size, resized_traveller.height // pixel_size),
        resample=Image.Resampling.NEAREST
    )
    pixelized_traveller = pixelized_traveller.resize(
        (pixelized_traveller.width * pixel_size, pixelized_traveller.height * pixel_size),
        resample=Image.Resampling.NEAREST
    )

    # Create the final image with the background-removed dragon and traveller overlaid on the pixelized image
    position_dragon = (pixelized_image.width - resized_dragon.width - 50, pixelized_image.height // 2 - resized_dragon.height - 100)
    final_image = pixelized_image.copy()
    final_image.paste(resized_dragon, position_dragon, resized_dragon)

    # Adjust the traveller position and paste it onto the final image
    position_traveller = (pixelized_image.width // 2 - pixelized_traveller.width - 400, pixelized_image.height - pixelized_traveller.height - 100)
    final_image.paste(pixelized_traveller, position_traveller, pixelized_traveller)

    # Plot histograms first
    plot_color_histograms(original_image, enhanced_image)
    
    # Display the images
    plt.figure(figsize=(14, 10))
    
    plt.subplot(3, 3, 1)
    plt.imshow(original_image)
    plt.axis('off')
    plt.title('Original Image')
    
    plt.subplot(3, 3, 2)
    plt.imshow(enhanced_image)
    plt.axis('off')
    plt.title('Enhanced Image')
    
    plt.subplot(3, 3, 3)
    plt.imshow(pixelized_image)
    plt.axis('off')
    plt.title('Pixelized Enhanced Image')

    plt.subplot(3, 3, 4)
    plt.imshow(dragon_image)
    plt.axis('off')
    plt.title('Dragon Image with Background')
    
    plt.subplot(3, 3, 5)
    plt.imshow(dragon_no_bg)
    plt.axis('off')
    plt.title('Dragon Image Without Background')

    plt.subplot(3, 3, 6)
    plt.imshow(final_image)
    plt.axis('off')
    plt.title('Final Image with Dragon (No BG)')
    
    plt.subplot(3, 3, 7)
    plt.imshow(traveller_image)
    plt.axis('off')
    plt.title('Traveller Image with Background')

    plt.subplot(3, 3, 8)
    plt.imshow(traveller_no_bg)
    plt.axis('off')
    plt.title('Traveller Image Without Background')

    plt.subplot(3, 3, 9)
    plt.imshow(final_image)
    plt.axis('off')
    plt.title('Final Image with Traveller (No BG)')
    
    plt.tight_layout()
    plt.show()

# Example usage
pixelize_and_display_images('Great_Wall_daytime.jpg', 'pixel dragon large.png', 'traveller.jpeg', pixel_size=10, color_enhancement_factor=2.0, dragon_resize_factor=0.5, traveller_resize_factor=0.7)
