'''
Requirements: Azure OpenAI gpt-4o key
'''


import pandas as pd
import numpy as np
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

"""
Functionality:-
This module is responsible for genertaing a more human friendly (better readability) response from the filtered dataframe.

Requirements:-
<1> doc named ./temp/data_description.txt having the information on all column features and values and what it represents (auto generation / human validation)
<2> filtered dataframe 

**args:-
<1> user query
<2> filtered dataframe
"""

load_dotenv()

def generate_response_from_filtered_data(dataframe,query):

    schema_info=""
    with open("temp/data_description.txt","r") as file:
        for reader in file.readlines():
            schema_info+=reader

    client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_4o_API_KEY"),  
    api_version = os.getenv("API_VERSION_4o"),
    azure_endpoint = os.getenv("AZURE_OPENAI_4o_ENDPOINT")
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
             You are responsible for explaining the answer to the user based on the dataframe, schema and the query provided to you.\
    The following dataframe is already filtered according to user query and columns renamed: {dataframe.to_csv(index=False)} \
    Do not assume any value, answer from the above dataframe only. \
    Return 'No Data Found' if you receive an empy dataframe. \
    This is the description of original dataset: {schema_info} \
    If query cannot be answered from the provided data, simply explain the reason for the same \
    Do not include any reasonings and warnings, directly respond to the query. \
    Do not alter placeholder values . \
    Do not remove angular brackets <>, keep those values as it is. \
    """} ,
    

    {"role": "user", "content": f"{query}"},

        ]
    )

    RESPONSE=response.choices[0].message.content

    return RESPONSE
