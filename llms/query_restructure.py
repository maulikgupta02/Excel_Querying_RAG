'''
 Contacts - Maulik Gupta OBS/MKT, Pushpendra Singh OBS/MKT
'''


import pandas as pd
import numpy as np
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

"""
Functionality:-
This module is responsible for restructuring the user query to best fit the table attributes to the user request.

Requirements:-
<1> doc named ./temp/InfoChest containing all column names and their unique values (generated automatically)

**args:-
<1> user query
"""

load_dotenv()

def generate_query(query):
    dfvalues=""
    with open("temp/InfoChest.txt","r") as file:
        for reader in file.readlines():
            dfvalues+=reader


    client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_4o_API_KEY"),  
    api_version = os.getenv("API_VERSION_4o"),
    azure_endpoint = os.getenv("AZURE_OPENAI_4o_ENDPOINT")
    )


    response = client.chat.completions.create(
        model="gpt-4o", # model = "deployment_name".
        messages=[
            {"role": "system", "content": f"""You have a dataframe information as an input. \
        It contains column namea and the unique values of all the columns. \

    {dfvalues}

    Don't asssume any other column and feature name, it should be exactly the same. \
    Given a user query, replace the given column names and the column values with the actual ones from that column, make sure to not remove anything. \
    Do not alter placeholder values . \
    Do not change or replace values within <> . \
    Restructure the query for better understanding of columns and its values. \
    Just give the new query directly"""},

    {"role": "user", "content": f"{query}"},


        ]
    )

    script=response.choices[0].message.content

    return script