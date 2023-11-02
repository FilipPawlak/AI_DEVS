#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 07:28:47 2023

@author: filippawlak
"""

import os
import openai
import requests


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

def moderation(input_data):
    json_send = {'input':input_data}
    headers = {"Content-Type" :"application/json" ,"Authorization": f"Bearer {openai.api_key}"}
    r = requests.post('https://api.openai.com/v1/moderations', json=json_send, headers=headers)
    response = (r.json())
    # print('Token:')
    print(response)
    try:
        return response['results'][0]['flagged']
    except Exception as e:
        raise Exception(e)



auth_cookie = get_auth('moderation')
task_json = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)
input_list = task_json['input']

moderation_check = [moderation(prompt) for prompt in input_list]
moderation_check = [int(prompt) for prompt in moderation_check]
print(moderation_check)


send_response(moderation_check, auth_cookie)
