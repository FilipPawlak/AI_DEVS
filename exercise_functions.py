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
    

auth_cookie = get_auth('functions')

response = get_task('https://zadania.aidevs.pl/task/' + auth_cookie)


client = OpenAI()
def ask_chat(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        max_tokens = 200,
        messages=[
    {"role": "system", "content": """Your are senior python enginner. Your role
     is to take a deep breath and going step by step create a function as per 
     user instructions. Make sure the output code has no bugs in it. Please
     respond wtih code and nothing else"""},
    {"role": "user", "content": prompt}]
    )
    print('#######GPT Response########')
    print(completion.choices[0].message.content)
    print('###########################')
    return completion.choices[0].message.content


answer = ask_chat(response['msg'])

send_response("""def addUser(name: str, surname: str, year: int) -> object:
    return {"name": name, "surname": surname, "year": year}""", auth_cookie)
 
