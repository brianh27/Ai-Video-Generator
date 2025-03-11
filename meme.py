import subprocess
from apicalls import meme
import time
from system import clear_folder,memeify

clear_folder('images')    
t=meme()
time.sleep(2)
memeify(t)

command = [
    'python', 'upload_video.py',
    '--file=output.mp4',
    f'--title={'The MEME award goes to...'}',
    '--description=Please Like and Subscribe for more amazing content!',
    '--keywords=viral,shorts',
    '--category=22',
    '--privacyStatus=public'
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

exit()