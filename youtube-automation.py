'''
    * Developed by Momin Baig
'''

'''
    1. Imports
'''
import os
import gtts
import math
import argparse
import requests
from bardapi import Bard, SESSION_HEADERS
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip

'''
    2. Main Functionality
'''

parser = argparse.ArgumentParser(description='A Youtube Automation Script by Momin Baig')
parser.add_argument('topic',help="Topic name.")
args=parser.parse_args()

topic = args.topic

file_name = topic.split(' ')
for idx, word in enumerate(file_name):
    file_name[idx] = word.lower()
file_name = '_'.join(file_name)

lang = 'en'
dir = topic.split(' ')
no_of_images = 0


# Bard Third-party API Package to scrape Script
token=""

session = requests.Session()
session.cookies.set("__Secure-1PSID", "")
session.cookies.set( "__Secure-1PSIDCC", "")
session.cookies.set("__Secure-1PSIDTS", "")
session.headers = SESSION_HEADERS

bard = Bard(token=token, session=session)
refine = bard.get_answer(f"Please write me a minute long speech on {topic} in simple words and one paragraph")['content'].split('\n')[2:-3]
text = ''.join(refine)


# Generating Audio
audio = gtts.gTTS(lang=lang, text=text, slow=False)
audio.save(f'audios/{file_name}.mp3')

audio_path = f"C:\\Users\\momin.baig\\Desktop\\youtube-automation\\audios\\{file_name}.mp3"
print(audio_path)
audio = AudioSegment.from_file(audio_path) 
audio_length = math.ceil(len(audio)/1000)

no_of_images = math.ceil(audio_length / 5)


# Dowloading Images of the Relevant Topic
os.system(f'bbid.py {topic} --limit {no_of_images} -o ./images/{file_name} --filters +filterui:aspect-wide')


# Compiling the images into a video
os.system(f'ffmpeg -framerate 1/5 -pattern_type glob -i "images/{file_name}/*.jpg" -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" -pix_fmt yuv420p videos/{file_name}.mp4')


# Merging the Video and Audio into a Single Clip
video = VideoFileClip(f'videos/{file_name}.mp4')
audio = AudioFileClip(f'audios/{file_name}.mp3')

video = video.set_audio(audio)
video.write_videofile(f'videos/{file_name}_final.mp4', codec='libx264')

os.system(f'rm videos/{file_name}.mp4')
