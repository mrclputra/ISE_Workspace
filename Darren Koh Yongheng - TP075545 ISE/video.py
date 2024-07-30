import os
from moviepy.editor import ImageSequenceClip, ImageClip, CompositeVideoClip, AudioFileClip
import re

# Path to the folder containing the frames
frames_folder = 'Video_Effect\\Dust_NB'

# Path to the static background image
background_image_path = 'Output\\combined_image.png'

# Path to the audio file
audio_file_path = 'Sound_Effect\\Wind_Blowing_Sound_Effect.mp3'

# Path to save the final video
output_video_path = 'Output\\Scene1.mp4'

# Frame rate of the final video
fps = 24

# Function to extract the numeric part of the file name
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# Get a list of the frame file paths sorted by the numeric part of the filename
frames = sorted(
    [os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if f.endswith('.png')],
    key=lambda x: extract_number(os.path.basename(x))
)

print(frames)  # For debugging, prints the sorted list of frames

# Create an ImageSequenceClip from the frames
frames_clip = ImageSequenceClip(frames, fps=fps)

# Explicitly set the duration of the frames clip
frames_duration = frames_clip.duration

# Create an ImageClip for the background image and set its duration to match the frames clip
background_clip = ImageClip(background_image_path).set_duration(frames_duration)

# Overlay the frames onto the background
final_clip = CompositeVideoClip([background_clip, frames_clip.set_position("center")])

# Load the audio file
audio_clip = AudioFileClip(audio_file_path)

# Set the audio of the final clip
final_clip = final_clip.set_audio(audio_clip)

# Write the final video to a file
final_clip.write_videofile(output_video_path, codec='libx264')
