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
This module is responsible for generating a pandas query to filter the original dataframe according to the user query.

Requirements:-
<1> doc named ./temp/data_description having the information on all column features and values and what it represents (auto generation / human validation)

**args:-
<1) user query
"""


load_dotenv()

def generate_response(query):
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
            {"role": "system", "content": f"""You have access to a pandas dataframe named df. \
    Here is a name and decription of each column in the dataframe

    {schema_info}

    Don't asssume any other column and feature name, it should be exactly the same. \
    Given a user question about the dataframe,Provide only the Python code to answer it.\
    Do not give any placeholders. \
    Don't assume you have access to any libraries other than built-in Python ones and pandas only. \
    You don't have any other data source other than dataframe df. \
    Make sure to refer only to the variables mentioned above. \
    Give the script to wrap it inside the custom function name generated_response(). \
    Return a single, new dataframe with only relevant and suitable column names according to the user query without modifying df \
    Return only required columns. \
    Do not add any print statements. \
    Do not alter placeholder values . \
    DO NOT REMOVE ANGULAR BRACKETS"""},

    {"role": "user", "content": f"{query}"},


        ]
    )

    # Extract the python script from generated response
    script=response.choices[0].message.content
    temp=script.split("```")[1]
    script=temp[6:]

    return script
