import os
import openai
import json
from openai import OpenAI
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
    

auth_cookie = get_auth('embedding')

get_task('https://zadania.aidevs.pl/task/' + auth_cookie)

response = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)


client = OpenAI()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   response = client.embeddings.create(input = [text], model=model)
   json_object = json.loads(response.json()) #to fix if string is returned instead of json
   return json_object['data'][0]['embedding']
   
embedding = get_embedding("Hawaiian pizza", model='text-embedding-ada-002')

print(len(embedding)) # to check if there are 1536 elements



send_response(embedding, auth_cookie)
 
