#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 08:44:04 2023

@author: filippawlak
"""

import os
import openai
import json
from openai import OpenAI
import requests
import pinecone   


client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")
ai_devs_data = {'apikey': os.getenv("AI_DEVS_API")}

#Creating connection with pinecone db
pinecone.init(      
	api_key=os.getenv("PINECONE_API"),      
	environment='gcp-starter'      
)      
index = pinecone.Index('test')

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

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   response = client.embeddings.create(input = [text], model=model)
   json_object = json.loads(response.json()) #to fix if string is returned instead of json
   return json_object['data'][0]['embedding']    

def search_vector_db(input_vector):
    response = index.query(
      vector=input_vector,
      top_k=1,
      include_values=False
)
    return response

#Getting cookie for exercise
auth_cookie = get_auth('search')
#Getting exercise data based on cookie
response = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)
print('#########')
print(response['question'])
print('#########')
#Converting question into embedding   
embedding = get_embedding(response['question'], model='text-embedding-ada-002')
#Searching by nearest vector in db
answer = search_vector_db(embedding)
response = answer['matches'][0]['id']
print(response)

send_response(response, auth_cookie)

