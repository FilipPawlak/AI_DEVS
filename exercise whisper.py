# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 11:18:09 2023

@author: filip
"""

import os
import openai
import json
from openai import OpenAI
import requests
import re
import vlc
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC') #path to VLC on PC

openai.api_key = os.getenv("OPENAI_API_KEY")
ai_devs_data = {'apikey': os.getenv("AI_DEVS_API")}

client = OpenAI()

def get_auth(task_name):
    r = requests.post(f'https://zadania.aidevs.pl/token/{task_name}', json=ai_devs_data)
    print(r.json())
    if r.json()['token']:
        token = (r.json()['token'])
        print('Returning token:')
        print(token)
        return token

def get_task(task_name):
    r = requests.get(task_name)
    response = r.json()
    print(response)
    return response

        
def send_response(answer, cookie):
    json_send = {'answer':answer}
    r = requests.post(f'https://zadania.aidevs.pl/answer/{cookie}', json=json_send)
    token = (r.json())
    print(token)
    return token
    
def get_audio_file(task, play_mode=False):
    print('#######################')
    print(task["msg"])
    print('#######################')
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    url_list = url_pattern.findall(task["msg"])
    url = url_list[0] #for this exercise we take only first founded link
    if play_mode:
        print(f'Playing: {url}')
        vlc.MediaPlayer(url).play()
    return url

def save_mp3_locally(url, file_name):
    doc = requests.get(url)
    with open(file_name, 'wb') as f:
            f.write(doc.content)

def whisper(mp3_url):
    audio_file= open(mp3_url, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )
    return transcript



auth_cookie = get_auth('whisper')

task = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)

url = get_audio_file(task, play_mode=False) #extract audio and play it

local_mp3_name = 'whisper_exercise_file.mp3'
save_mp3_locally(url, local_mp3_name) #saving mp3 to my pc


transcription = whisper(os.getcwd()+ '//' + local_mp3_name) #passing downloaded mp3 into whisper
    
send_response(transcription.text, auth_cookie) #sending respones
     
