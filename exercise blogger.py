#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 07:48:13 2023

@author: filippawlak
"""

import os
import openai
import requests
import time
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")
ai_devs_data = {'apikey': os.getenv("AI_DEVS_API")}

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

client = OpenAI()
def ask_chat(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        max_tokens = 250,
        messages=[
    {"role": "system", "content": """ou are a blogger and you respond with blog post in polish about outline provided by the user.
     Remember to stick to the topic provided by the user and write reponse always in polish language!"""},
    {"role": "user", "content": prompt}]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

start = time.time()
auth_cookie = get_auth('blogger')
task_json = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)
input_list = task_json['blog']

blog_enttries = [ask_chat(prompt) for prompt in input_list]

send_response(blog_enttries, auth_cookie)

end = time.time()
print(end - start)



