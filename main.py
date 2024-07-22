import streamlit as st
import pandas as pd
import numpy as np
from anonymizer import *
from llms.query_restructure import generate_query
from llms.filter_table import generate_response
from llms.response import generate_response_from_filtered_data


st.set_page_config(page_title="Security Use-Case",layout="wide")

st.markdown("# Security Use-Case")
# st.sidebar.markdown("# Architecture-01")

st.header('Device information at your fingertips !', divider='orange')

DATASET_KEY = 'dataset'
QUERIES_KEY = 'queries'
RESPONSES_KEY = 'responses'
RESPONSES_2_KEY = 'filtered_response'

# Load the dataset only if it is not already loaded
if DATASET_KEY not in st.session_state:
    with st.spinner('Loading dataset'):
        df = pd.read_parquet("processed_data/raw_data.parquet")                                 
        st.session_state[DATASET_KEY] = df
    st.success('Dataset Loaded Successfuly!')
else:
    df = st.session_state[DATASET_KEY]

# Display the dataset head
st.title("A Glimpse of the Dataset")
st.write(df.head())

# Initialize session state lists for queries and responses if they don't exist
if QUERIES_KEY not in st.session_state:
    st.session_state[QUERIES_KEY] = []

if RESPONSES_KEY not in st.session_state:
    st.session_state[RESPONSES_KEY] = []

if RESPONSES_2_KEY not in st.session_state:
    st.session_state[RESPONSES_2_KEY] = []

st.write("chat history")
with st.container(height=None,border=True):
    for query, response_, filtered_response in zip(st.session_state[QUERIES_KEY], st.session_state[RESPONSES_KEY], st.session_state[RESPONSES_2_KEY]):
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            st.write(response_)
        with st.chat_message("assistant"):
            st.write(filtered_response)

st.markdown("##")

# Chat input
query = st.chat_input("Ask Away !")

if query:
    # Append the new query to session state
    st.session_state[QUERIES_KEY].append(query)
    anonymized_query=anonymize_text(query)
    restructred_query_anonymized = generate_query(anonymized_query)

    
    with st.chat_message("user"):
        st.write(query)
    
    with st.spinner("hmmm..let me think!!!"):
        error=""
        counter=0
        flag=1
        while True:
            try:
                anonymized_query=anonymize_text(query)
                restructred_query_anonymized = generate_query(anonymized_query)
                print(restructred_query_anonymized) #for debugging
                st.write(f"""
                        This is what I understood: \
                        {deanonymize_text(deanonymize_text(restructred_query_anonymized))}
                """)
                anonymized_prompt=generate_response("Provide only the Python code wrapped inside the function generated_response() with no args to "+restructred_query_anonymized+error+" and generate a dataframe")
                prompt=deanonymize_text(anonymized_prompt)
                print(prompt) #for debugging
                exec(prompt)
                RESPONSE=generated_response() #not an error-->he's lying believe me (;
                print(RESPONSE)
                break
            except Exception as e:
                print(e)
                error=f"""got error as {e} on your previous response {prompt}, give correct code"""
                pass
            counter+=1
            if counter>=5:
                RESPONSE="No related information found in the dataframe"
                flag=0
                break

        RESPONSE_to_store=RESPONSE.copy()
        with st.chat_message("assistant"):
            st.write(RESPONSE)
        st.session_state[RESPONSES_KEY].append(RESPONSE_to_store)

        if flag: 

            if RESPONSE.shape[0]*RESPONSE.shape[1] > 5000:
                st.write("Cannot be processsed further due to large size")
                st.session_state[RESPONSES_2_KEY].append("Cannot be processsed further due to large size")

            else:
                filtered_RESPONSE=deanonymize_text(generate_response_from_filtered_data(dataframe=anonymize_dataframe(RESPONSE),query=anonymized_query))
                with st.chat_message("assistant"):
                    st.write(filtered_RESPONSE)

                st.session_state[RESPONSES_2_KEY].append(filtered_RESPONSE)

    

    # st.write("chat history")
    # with st.container(height=None,border=True):
    #     for query, response in zip(st.session_state[QUERIES_KEY], st.session_state[RESPONSES_KEY]):
    #         with st.chat_message("user"):
    #             st.write(query)
    #         with st.chat_message("assistant"):
    #             st.write(response)
