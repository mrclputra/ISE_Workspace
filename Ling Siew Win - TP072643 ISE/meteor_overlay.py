import cv2
import numpy as np
from PIL import Image

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def resize_frame(frame, size):
    return cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

def create_sky_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 120])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    return mask

def create_landmark_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    return mask

def refine_landmark_mask(landmark_mask):
    h, w = landmark_mask.shape
    cv2.rectangle(landmark_mask, (int(w*0.45), int(h*0.35)), (int(w*0.55), int(h*0.65)), (255), thickness=cv2.FILLED)
    return landmark_mask

def create_exclusion_zone_mask(image):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    h, w = mask.shape
    cv2.rectangle(mask, (0, int(h*0.5)), (int(w*0.5), h), (255), thickness=cv2.FILLED)  # Bottom left exclusion zone
    cv2.rectangle(mask, (int(w*0.65), int(h*0.3)), (w, h), (255), thickness=cv2.FILLED)  # Middle right exclusion zone
    return mask

def overlay_frames_on_image(image_path, frames, output_path, traveler_image_path, opacity=0.5):
    base_image = cv2.imread(image_path)
    if base_image is None:
        print(f"Error: Couldn't open base image file at {image_path}")
        return
    
    # Load the background-removed traveler image
    traveler_image = cv2.imread(traveler_image_path, cv2.IMREAD_UNCHANGED)
    traveler_image_resized = cv2.resize(traveler_image, (200, 200), interpolation=cv2.INTER_AREA)

    sky_mask = create_sky_mask(base_image)
    landmark_mask = create_landmark_mask(base_image)
    landmark_mask = refine_landmark_mask(landmark_mask)
    
    exclusion_zone_mask = create_exclusion_zone_mask(base_image)
    
    combined_mask = cv2.bitwise_and(sky_mask, cv2.bitwise_not(landmark_mask))
    combined_mask = cv2.bitwise_and(combined_mask, cv2.bitwise_not(exclusion_zone_mask))

    WIDTH, HEIGHT = base_image.shape[1], base_image.shape[0]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (WIDTH, HEIGHT))

    for frame in frames:
        resized_frame = resize_frame(frame, (WIDTH, HEIGHT))
        
        meteor_overlay = cv2.bitwise_and(resized_frame, resized_frame, mask=combined_mask)
        
        inverse_combined_mask = cv2.bitwise_not(combined_mask)
        background = cv2.bitwise_and(base_image, base_image, mask=inverse_combined_mask)
        
        combined = cv2.addWeighted(base_image, 1, meteor_overlay, opacity, 0)
        final_frame = cv2.bitwise_or(combined, background)
        
        # Overlay the traveler image on the final frame
        traveler_alpha_channel = traveler_image_resized[:, :, 3] / 255.0
        traveler_rgb_channels = traveler_image_resized[:, :, :3]

        # Expand the alpha channel to match the dimensions of the RGB channels
        traveler_alpha_channel = np.repeat(traveler_alpha_channel[:, :, np.newaxis], 3, axis=2)

        # Calculate the position where the traveler image will be placed
        traveler_y_start = HEIGHT - traveler_image_resized.shape[0] - 50
        traveler_y_end = traveler_y_start + traveler_image_resized.shape[0]
        
        # Move the traveler to the bottom middle with an offset to the left
        traveler_x_start = (WIDTH - traveler_image_resized.shape[1]) // 2 - 180
        traveler_x_end = traveler_x_start + traveler_image_resized.shape[1]

        # Ensure the traveler image fits within the final frame
        traveler_y_end = min(traveler_y_end, HEIGHT)
        traveler_x_end = min(traveler_x_end, WIDTH)
        
        # Calculate the correct slicing dimensions
        traveler_slice_y_end = traveler_y_end - traveler_y_start
        traveler_slice_x_end = traveler_x_end - traveler_x_start

        final_frame[traveler_y_start:traveler_y_end, traveler_x_start:traveler_x_end] = \
            final_frame[traveler_y_start:traveler_y_end, traveler_x_start:traveler_x_end] * (1 - traveler_alpha_channel[:traveler_slice_y_end, :traveler_slice_x_end]) + \
            traveler_rgb_channels[:traveler_slice_y_end, :traveler_slice_x_end] * traveler_alpha_channel[:traveler_slice_y_end, :traveler_slice_x_end]
        
        out.write(final_frame)
        
        # Optional: Display the comparison frame
        comparison_frame = np.hstack((base_image, final_frame))
        cv2.imshow('Comparison Frame', comparison_frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'meteor_source.mp4'
image_path = 'Great_Wall_night.jpg'
output_path = 'greatwall_meteor.mp4'
traveler_image_path = 'traveller_no_bg.png'

frames = extract_frames(video_path)
overlay_frames_on_image(image_path, frames, output_path, traveler_image_path)