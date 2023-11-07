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
auth_cookie = get_auth('inprompt')
exercise = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)
question = exercise['question']
print('###############')
print('The question is:')
print(question)
print('###############')

#Using LLM to determine name of a person mentioned in question
completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": """"Your role is to return name of a 
     character present in the question from user. Please return only name
     and nothing else as it will be used to prepare context for another prompt"""},
    {"role": "user", "content": f'{question}'}
  ]
)

#Printing name of person mentioned in question
response = completion.choices[0].message["content"]
print(response)
print('###############')

#Creating list with senteces, which are about above mentioned person
important_context = [x for x in exercise['input'] if response in x]

if len(important_context) == 0:
    raise Exception('No context to answer the question')

#Printing information we have at this step - name of character and sentences
#about him
print(f'Sentences about {response}')
print(important_context)

#Using LLM to answer the question using filtered out context
completion2 = openai.ChatCompletion.create(
  model="gpt-4",# may be switched to 3.5-turbo to reduce costs
  messages=[
    {"role": "system", "content": f""""Please answer the question based
     on following information:
    {important_context}"""},
    {"role": "user", "content": f'{question}'}
  ]
)
final_response = completion2.choices[0].message["content"]
print('Final response')
print(question)
print(final_response)
send_response(final_response, auth_cookie)
