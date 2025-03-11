import time
import requests
import json

from pydub import AudioSegment
import base64
import mimetypes
import requests
import subprocess
import os
import io
from openai import OpenAI
from PIL import Image
from io import BytesIO
import shutil

def clear_folder(folder_path):
    
    if not os.path.exists(folder_path):
        print(f"The folder \"{folder_path}\" does not exist.")
        return
    try:
        os.remove('output.mp4')
        print("output.mp4 has been deleted.")
    except OSError:
        print("output.mp4 does not exist or cannot be deleted.")
    # Remove all files and subdirectories in the folder
    for file_or_dir in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_or_dir)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)  # Remove the file or symlink
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)  # Remove the directory
        except Exception as e:
            print(f"Failed to delete {full_path}: {e}")

    print(f"All contents of the folder \"{folder_path}\" have been cleared.")
def memeify(image_path):
    video_path = "video.mp4"   
    
    output_path = "output.mp4" 

    overlay_x = "(W-w)/2"
    overlay_y = "0"  

    
    video_duration = 4.5

    # FFmpeg command to overlay an image at the top and scale it
    command = [
    "ffmpeg",
    "-i", video_path,   # Input video
    "-i", image_path,   # Overlay image
    "-filter_complex",
    f"[1:v] scale=1080:-1:force_original_aspect_ratio=decrease [overlay];"
    f"[0:v][overlay] overlay={overlay_x}:{overlay_y}",
    "-t", str(video_duration),  # Set total video duration to 4.5 seconds
    "-c:v", "libx264",  # Use H.264 codec for video
    "-c:a", "aac",      # Use AAC codec for audio
    "-strict", "experimental",
    output_path
    ]

    
    try:
        subprocess.run(command, check=True)
        print(f"Output saved as {output_path}")
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e)

def overlay_video_on_images(video_path, file_names, output_path, times, audio_path, captions,length):
    # Creating filter_complex to alternate the images
    
    command = [
        'ffmpeg',
        '-analyzeduration', '200M',  # Increase analyzeduration
        '-probesize', '100M',        # Increase probesize
        '-i', video_path,           # Input video
        '-i', audio_path            # Input audio
    ]
    for a in file_names:
        command.append('-i')
        command.append(a)
    command.append("-filter_complex")
    filter_complex=""""""
    
    for a in range(len(file_names)):
        filter_complex+=f"[{2+a}:v]scale=w=1080:h=-1:force_original_aspect_ratio=increase[{a}];"    
    start='[0:v]'
    num=0
    for a in range(len(file_names)):
        filter_complex+=(start+f"[{a}]overlay=0:0:enable='between(t,{times[a]},{times[a+1]})'[out{a}];")
        start=f'[out{num}]'
        num+=1
    for a in range(len(captions)-1):
        filter_complex+=(start+f"drawtext=text={captions[a][1]}:x=(w-text_w)/2:y=(h-text_h)/2:fontcolor=white:fontsize=80:enable='between(t,{captions[a][0]},{captions[a+1][0]})'[out{num}];")
        start=f'[out{num}]'
        num+=1
    filter_complex+="[0:a][1:a]amix=inputs=2:duration=first[audio_out]"
    print(filter_complex)
    
    
    command.extend([ filter_complex,  # Apply the video and text filters
        "-map", start, "-map", "[audio_out]", "-t", str(length), "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
    "output.mp4"])

    # Run the command and capture errors
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e)

