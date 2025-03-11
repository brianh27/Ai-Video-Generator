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
def extension(format_name):
    print(format_name)
    
    if format_name == "jpeg":
        return ".jpg"
    elif format_name == "png":
        return ".png"
    elif format_name == "gif":
        return ".gif"
    elif format_name == "bmp":
        return ".bmp"
    elif format_name == "webp":
        return ".webp"
    elif format_name == "tiff":
        return ".tif"
    else:
        return ".bin"  # Fallback for unknown formats
def fetch_images_from_google(prompt,num):
    
    
    api_key = 'AIzaSyBqvs80rmSAz5VCUYoW-AMUV347QnFfqCE'
    cx = 'f59ad213ea49b4e52'
    url = 'https://www.googleapis.com/customsearch/v1'
    
    
    params = {
        'key': api_key,
        'cx': cx,
        'q': prompt,
        'searchType': 'image'
    }
    
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['items'][num]['link']  # Return the JSON response
    else:
        print(f"Error: {response.status_code}")
        return None
def fetch_pexels(prompt,num):
    API_KEY = "9JZnQJQ1Gm1KYyMDEZjcoRnTMiupPZidsStDw2Wf8XQHljHuCIPT3S9S"
    url = f"https://api.pexels.com/v1/search?query={prompt}&per_page={num}&orientation=landscape"

    
    headers = {
        "Authorization": API_KEY
    }

    
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  
        return data['photos'][-1]["src"]['original']
    else:
        print(f"Error: {response.status_code}, {response.text}")
def download(num,filename,a):
    
    # Image URL
    if filename[a][-1]=='^':

        url = fetch_pexels(filename[a][:-1],num)
    else:
        url = fetch_pexels(filename[a][:-1],num)
    
    if url==None:
        
        return download(num+1,filename,a)
    print(url)

    
    
  
    try:
        # Fetch the image from a URL
        response = requests.get(url)
        
        image_data = io.BytesIO(response.content)
        width,height=Image.open(image_data).size
        if abs(width/height-1.7)>0.5:
            print('Dimensions Wrong')
            
            return download(num+1,filename,a)
        
        # Run ffmpeg to check if the image can be processed (without saving the file)
        command = ['ffmpeg', '-f', 'image2', '-i', 'pipe:0', '-t', '1', '-f', 'null', '-']  # Use 'pipe:0' for input from memory

        # Run the subprocess command and pass the image data
        result = subprocess.run(command, input=image_data.read(), capture_output=True)

        # Check if there was an error opening the image file
        if result.stderr:
            pass
        else:
            print("Error in opening file "+a)
            download(num+1,filename,a)
            return
        
        name=filename[a]+extension(Image.open(BytesIO(response.content)).format.lower())
        name = os.path.join('images', name)
        filename[a]=name
        
        with open(name, "wb") as file:
            file.write(response.content)
        return filename
    except Exception as e:
        print(f"Failed to download image. Status code: {e}")
        return download(num+1,filename,a)
        
