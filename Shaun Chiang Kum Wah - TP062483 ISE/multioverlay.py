from PIL import Image

def overlay_multiple_images(base_image_path, overlay_images_info, output_image_path):
    """
    Overlay multiple images on top of a base image.

    :param base_image_path: Path to the base image.
    :param overlay_images_info: List of tuples, each containing:
                                 - path to the overlay image
                                 - offset (x, y) for the overlay image
                                 - resize factor (optional, default is 1.0)
    :param output_image_path: Path where the output image will be saved.
    """
    # Load the base image
    base_image = Image.open(base_image_path).convert('RGBA')
    
    # Create a new image with a size that can accommodate all images
    base_width, base_height = base_image.size
    
    # Calculate the required size for the new image
    for overlay_path, offset, resize_factor in overlay_images_info:
        overlay_image = Image.open(overlay_path).convert('RGBA')
        
        # Resize the overlay image if a resize factor is provided
        if resize_factor != 1.0:
            overlay_width, overlay_height = overlay_image.size
            new_size = (int(overlay_width * resize_factor), int(overlay_height * resize_factor))
            overlay_image = overlay_image.resize(new_size, Image.Resampling.LANCZOS)
        
        overlay_width, overlay_height = overlay_image.size
        new_width = max(base_width, overlay_width + offset[0])
        new_height = max(base_height, overlay_height + offset[1])
        base_width = new_width
        base_height = new_height
    
    # Create a new image with a transparent background
    new_image = Image.new('RGBA', (base_width, base_height), (0, 0, 0, 0))
    
    # Paste the base image onto the new image
    new_image.paste(base_image, (0, -200))
    
    # Overlay each image
    for overlay_path, offset, resize_factor in overlay_images_info:
        overlay_image = Image.open(overlay_path).convert('RGBA')
        
        # Resize the overlay image if a resize factor is provided
        if resize_factor != 1.0:
            overlay_width, overlay_height = overlay_image.size
            new_size = (int(overlay_width * resize_factor), int(overlay_height * resize_factor))
            overlay_image = overlay_image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Paste the overlay image onto the new image with the specified offset
        new_image.paste(overlay_image, offset, overlay_image)
    
    # Save the resulting image
    new_image.save(output_image_path, format='PNG')

    print(f"Composite image saved as {output_image_path}")

# Example usage
base_image_path = 'Shaun Chiang Kum Wah - TP062483 ISE/components/BandofLightGoetia.png'       # Path to the base image
overlay_images_info = [
    ('Shaun Chiang Kum Wah - TP062483 ISE/components/Tower3.png', (0, 0), 1),  # Path, offset, resize factor
    ('Shaun Chiang Kum Wah - TP062483 ISE/components/car_base.png', (1200, 830), 0.2), # Path, offset, resize factor
    ('Shaun Chiang Kum Wah - TP062483 ISE/components/time_traveller.png', (1200, 840), 0.2)  # Path, offset, resize factor

]
output_image_path = 'Shaun Chiang Kum Wah - TP062483 ISE/components/overlayed.png'   # Path where the output image will be saved

overlay_multiple_images(base_image_path, overlay_images_info, output_image_path)
