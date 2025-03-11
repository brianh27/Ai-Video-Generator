import random
import time
import requests
import json
from supabase import create_client
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
import httpx
def audio(text):
    output_file='draft.mp3'
    client = OpenAI()

    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    
    if hasattr(response, 'iter_bytes'):  
        with open(output_file, "wb") as file:
            # Stream and write chunks to the file as they're received
            for chunk in response.iter_bytes():
                file.write(chunk)

    return output_file
def speechify(text):
    base = "https://api.sws.speechify.com"

    url=f"{base}/v1/audio/speech"
    key = "CPM4aX11sy0RdKWSXiUe1QIE4tAFOty8o_3uCAxIPpY="  
    voice = "mrbeast"     
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    data = {
        "input": f"<speak>{text}</speak>",
        "voice_id": voice,
        "audio_format": "mp3",
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    
    response_data = response.json()
    audio_data = base64.b64decode(response_data["audio_data"])


    return audio_data
def call(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

def callsupa():
    url = "https://qtlmcbfrdfqxpsfmdehb.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0bG1jYmZyZGZxeHBzZm1kZWhiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY4MzIwNjAsImV4cCI6MjA1MjQwODA2MH0.o0QTSOc1NJc5iQGfJcyftldknN6ZKzC0wqXN5Q8_EDM"
    supabase = create_client(url, key)

    table_name = "Tasks" 
    response = supabase.table(table_name).select("*").limit(10).execute()
    print(response.data)
    if response.data:
        return response.data  # Return the first row
    return "Generate a random topic. Then generate a set of 5 interesting facts about it. Then list the facts in a numbered list. Include one fact at the end that exactly writes: it is impossible to subscribe with your eyes closed."  # Return None if no data is found
def meme():
    url = "https://api.imgflip.com/get_memes"

    
    response = requests.get(url)
    
    
    
    if response.status_code == 200:
        data = response.json()  
        
    else:
        print(f"Error: {response.status_code}")
        return None
    list=data["data"]["memes"]
    while True:
        memes=list[random.randint(0,len(list)-1)]
        if 1.5<memes['width']/memes['height']<3:
            break
    link='https://i.imgflip.com/'+memes['url'].split('/')[-1]
    response = requests.get(link, stream=True)
        
    if response.status_code == 200:
        

        image_path = os.path.join('images',memes['url'].split('/')[-1] )
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
                print(f"Image saved at: {image_path}")
        return image_path
    else:
        print(f"Failed to download image. Status Code: {response.status_code}")
        
        print(data)  