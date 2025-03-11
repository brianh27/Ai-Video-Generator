from apicalls import speechify
import time
import subprocess
from apicalls import callsupa
for _ in range(50):
    subject=callsupa()
    if subject=='STOP':
        exit()
    try:
        subprocess.run(['python', 'meme.py'], check=True)  
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")