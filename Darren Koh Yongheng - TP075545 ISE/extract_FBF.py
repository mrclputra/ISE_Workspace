import cv2
import numpy as np
import os

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"{frame_count}.png")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()

def make_black_background_transparent(input_folder, output_folder, lower_bound, upper_bound):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            frame_path = os.path.join(input_folder, filename)
            frame = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)

            # Convert BGR to BGRA (adding an alpha channel)
            b, g, r = cv2.split(frame)
            alpha = np.ones(b.shape, dtype=b.dtype) * 255  # Create alpha channel fully opaque

            # Create a mask for the specified color range
            lower_bound = np.array(lower_bound, dtype="uint8")
            upper_bound = np.array(upper_bound, dtype="uint8")
            mask = cv2.inRange(frame, lower_bound, upper_bound)
            
            # Set alpha to 0 for the masked areas
            alpha[mask != 0] = 0
            
            # Merge channels back
            frame_with_transparency = cv2.merge([b, g, r, alpha])
            frame_with_transparency = cv2.resize(frame_with_transparency, (1920, 1080))
            
            # Save the frame with transparency
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, frame_with_transparency)

video_path = 'Darren Koh Yongheng - TP075545 ISE\\Video_Effect\\dust.mp4'
extracted_frames_folder = 'Darren Koh Yongheng - TP075545 ISE\\Video_Effect\\Dust_FBF'
frames_with_transparency_folder = 'Darren Koh Yongheng - TP075545 ISE\\Video_Effect\\Dust_NB'

# Define lower and upper bounds for the color black (you can adjust these values)
lower_black = [0, 0, 0]
upper_black = [50, 50, 50]

extract_frames(video_path, extracted_frames_folder)
make_black_background_transparent(extracted_frames_folder, frames_with_transparency_folder, lower_black, upper_black)
