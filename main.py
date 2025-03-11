import httpx
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
from apicalls import call,audio,callsupa
from images import download
from volume import volume
from system import clear_folder,overlay_video_on_images




clear_folder('images')    

subject=callsupa()[0]['Commands']


if subject=='STOP':
    exit()
print(subject)
script = call(
        f"Write a well-crafted paragraph that can be spoken in 10-15 seconds. This is supposed to be a script for a youtube short, so make it engaging and to the point."
        f"Start directly with the content, without any title or introductory phrases. "
        f"Focus on the subject: {subject}. Ensure the paragraph is clear, engaging, and to the point."
    )
title=call(f"Give me a good title for this script {script}")

print(script)
audio_file=audio(script)
volume()
    
subprocess.run(['python','transcribe.py'],check=True)
with open('script.srt','r') as file:
    transcription=file.read()

timings = call(
            f"Here is the .srt file of the video {transcription}\n"
            "The script is provided above. Only return this:\n"
            "For each section of the script, give a relevant image description.\n"
            "On odd-numbered lines, provide the start time (in seconds), a dash, and the end time (in seconds).\n"
            "On even-numbered lines, provide a short, three-word general image description for the timing above. \n"
            "On the same even-numbered line. At the end write one character. ^ for if the image would be general and versatile - images that would appear on a stock image site. & for if the image is specific, personal, brand related - if a relevant image would better appear on google image search.\n"
            "Ensure each description corresponds to a common image concept that is engaging and highly relevant. Try to generate general images, the more general and the more common the image is the better\n"
            "Example format:\n"
            "0.000-11.235\nExtravagant stunts\n\n"
            "11.235-17.642\nPhilanthropic challenges\n\n"
            "17.642-22.954\nLarge-scale giveaways\n\n"
            "22.954-28.362\nFriends' involvement\n\n"
            "28.362-35.173\nGenuine acts\n"
            "Do not explain or justify your choices; provide only the formatted output.\n"
            "The descriptions must represent general but highly relevant images commonly found online."
        )

print(timings)

text = [line for line in timings.split('\n') if line.strip()]

file_name=[]
times=[0]
for a in range(len(text)):
    if a%2==0:
        times.append(float(text[a].split('-')[1]))
    else:
        file_name.append(text[a])
   
for a in range(len(file_name)):
    if os.path.exists(file_name[a]):
        print('Already has file')
        continue
    file_name=download(1,file_name,a)


audio_length = len(AudioSegment.from_file('audio.mp3')) / 1000

with open('transcript.json', 'r') as file:
    data = json.load(file)

captions=[]
for a in data["monologues"][0]['elements']:
    if a['type']=='text':

        captions.append((a['ts'],' '.join(a['value'].split("'"))))
captions.append((audio_length,'r'))


#with open('output.txt','w') as file:
 #   file.write(str(audio_length))

print(file_name)

overlay_video_on_images('video.mp4', file_name, 'output.mp4',times,'audio.mp3',captions,audio_length)
command = [
    'python', 'upload_video.py',
    '--file=output.mp4',
    f'--title={title}',
    '--description=Please Like and Subscribe for more amazing content!',
    '--keywords=facts,stories,fun,tiktok,viral,shorts',
    '--category=22',
    '--privacyStatus=public'
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

exit()