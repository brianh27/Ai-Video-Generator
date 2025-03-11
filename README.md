# Ai-Video-Generator
This is an AI Video Generator. It will generate short videos based on an initial prompt and automatically upload them to youtube.
Here is a sample video:
https://www.youtube.com/shorts/L_4m59yeZdo

The program goes through the following steps to generate the finished video:
1. Calls to an OpenAI API to generate the script based on a topic
2. Uses Speechify API to generate the AI audio for the script
3. Generates a transcription and captions with timing
4. These exact timings are plugged back into OPENAI API to generate image prompts for each segment (normally a few seconds) of the video
5. Images are extracted and downloaded from Pixabay API
6. Using FFMPEG, the entire video is put together
7. Using Youtube Data API v3, the video is uploaded, with custom titles and descriptions (Authentication process is needed only initially)

This process is done fully autonomously. You may simply leave your computer on and videos will be uploaded.
You may also run this program on a Rasberry Pi.

