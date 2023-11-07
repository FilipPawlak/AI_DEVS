#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 08:37:29 2023

@author: filippawlak
"""


import requests
import os
import openai

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
    
#Getting auth cookie
auth_cookie = get_auth('liar')

#Send question to enpoint
print('Please provide a question to AI_DEVS API')
question = input()
data={'question':question}
r = requests.post(('https://zadania.aidevs.pl/task/' + auth_cookie), data=data)
answer = r.json()['answer']

print(answer)

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Your role is to decide wheather the question relates to an answer. Please return only Yes or No answer"},
    {"role": "user", "content": f"question={question}, answer={answer}"}
  ]
)

response = completion.choices[0].message["content"]
print(response)

send_response(response, auth_cookie)
