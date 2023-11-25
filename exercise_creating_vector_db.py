#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:48:33 2023

@author: filippawlak
"""

import pinecone   
import os 
import requests  
import pandas as pd
from openai import OpenAI
import json
import tiktoken
import utils



#Pulling exercise data
r = requests.get('https://unknow.news/archiwum.json')
data = r.json()
data_pandas = pd.DataFrame(data)

client = OpenAI()


#Creating embedding
def get_embedding(text, model="text-embedding-ada-002"):
   response = client.embeddings.create(input = [text], model=model)
   json_object = json.loads(response.json()) #to fix if string is returned instead of json
   return json_object['data'][0]['embedding']



# Asses number of neededtokens
encoding = tiktoken.get_encoding('cl100k_base')
data_pandas['All_info'] = data_pandas.agg('|'.join, axis=1)
data_pandas["n_tokens"] = data_pandas['All_info'].apply(lambda x: len(encoding.encode(x)))
print(f'All needed tokens around: {data_pandas["n_tokens"].sum()}')


# data_pandas["embedding"] = data_pandas['All_info'].apply(lambda x: get_embedding(x))
# data_pandas.to_pickle('/Users/filippawlak/Desktop/AI_DEVS/AI_DEVS/exercise_embedding_temp.pkl')

#Loading embedding from pickle not to duplicate tokens usage
data_pandas = pd.read_pickle('/Users/filippawlak/Desktop/AI_DEVS/AI_DEVS/exercise_embedding_temp.pkl')


#Creating connection with pinecone db
pinecone.init(      
	api_key=os.getenv("PINECONE_API"),      
	environment='gcp-starter'      
)      
index = pinecone.Index('test')



#preparing data to insert
data = data_pandas[['url','embedding']].rename(columns={"url": "id", "embedding": "values"})
data['id'] = data['id'].astype(str)
data = data.head(300) #Just for this exercise 300 rows is enough
data = data.to_dict('records')

# Inserting records
upsert_response = index.upsert(
    vectors=data
)


# Example of upsert from docs
# index.upsert(
#   vectors=[
#     {"id": "A", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
#     {"id": "B", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
#     {"id": "C", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
#     {"id": "D", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]},
#     {"id": "E", "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}
#   ]
# )






