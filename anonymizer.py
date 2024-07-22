'''
 Contacts - Maulik Gupta OBS/MKT, Pushpendra Singh OBS/MKT
'''


"""
Presidio Anonymization Module

**args:-
<1> string/dataframe to be anonymized

requirements:-
<1> list of columns to anonymize
"""

from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from presidio_analyzer import PatternRecognizer, Pattern
import pandas as pd
import numpy as np

# store columns to anonymize in the ./temp directory under columns_to_anonymize.txt file.
columns_to_anonymize=np.loadtxt("temp/columns_to_anonymize.txt",dtype=str, delimiter=",").tolist()

dataset = pd.read_parquet('processed_data/raw_data.parquet')

anonymizer = PresidioReversibleAnonymizer(
    analyzed_fields=[], 
    faker_seed=42,
)

for column in columns_to_anonymize:
    anonymizer.add_recognizer(PatternRecognizer(supported_entity=f"{column}_placeholder",
                                                deny_list=list(dataset[column].unique()),
                                                deny_list_score=0.5)) 
    

def anonymize_text(text):
    """
    A decorator function to anonymize query for the dataframe.
 
    Args:
        func: query to be anonymized.
 
    Returns:
        anonymized text.
 
    Raises:
        "Invalid argument datatype !" If incorrect datatype in passed as input
    """

    if type(text)!=str:
        return "Invalid argument datatype !"
    return anonymizer.anonymize(text)



def anonymize_dataframe(df):
    """
    A decorator function to anonymize dataframe.
 
    Args:
        func: dataframe to be anonymized.
 
    Returns:
        anonymized dataframe.
 
    Raises:
        "Invalid argument datatype !" If incorrect datatype in passed as input
    """

    if type(df)!=pd.DataFrame:
        return "Invalid argument datatype !"
    for column in df.columns:
        if column in columns_to_anonymize:
            df[column] = df[column].astype(str)
            df[column] = df[column].apply(anonymizer.anonymize)

    return df



def deanonymize_text(text):
    """
    A decorator function to deanonymize query for the dataframe.
 
    Args:
        func: query to be deanonymized.
 
    Returns:
        deanonymized query.
 
    Raises:
        "Invalid argument datatype !" If incorrect datatype in passed as input
    """

    if type(text)!=str:
        return "Invalid argument datatype !"
    return anonymizer.deanonymize(text)



def deanonymize_dataframe(df):
    """
    A decorator function to deanonymize the dataframe.
 
    Args:
        func: dataframe to be deanonymized.
 
    Returns:
        deanonymized dataframe.
 
    Raises:
        "Invalid argument datatype !" If incorrect datatype in passed as input
    """

    if type(df)!=pd.DataFrame:
        return "Invalid argument datatype !"
    for column in df.columns:
        if column in columns_to_anonymize:
            df[column] = df[column].astype(str)
            df[column] = df[column].apply(anonymizer.deanonymize)

    return df
