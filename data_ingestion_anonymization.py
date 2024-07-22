"""
This module serves the following purposes:
    <1> Feature engineering on ingested excel file
    <2> Performs anonymization
    <3> Saves both raw and anonymized dataframes in csv format
    <4> Creates a document containing unique values for selected columns

To be run at the time of data ingestion
"""


# from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
# from presidio_analyzer import PatternRecognizer, Pattern
import pandas as pd
import numpy as np
import os

# # For dataframe only
# columns_to_anonymize = ["customer name","IC01 Code","sysname","TMKey","sdwan_ip_admin"] # list all the column names to anonymize
# columns_to_anonymize_deny_list = ["customer name","IC01 Code","sysname","TMKey","sdwan_ip_admin"] # list all the column names to anonymize via deny list


# Read data as dataframe
dataset = pd.read_excel("raw_data/Power BI data-Security.xlsx",skiprows=2)

columns_to_discard=np.loadtxt("temp/columns_to_discard.txt",dtype=str, delimiter=",").tolist()
columns_to_anonymize=np.loadtxt("temp/columns_to_anonymize.txt",dtype=str, delimiter=",").tolist()


dataset.drop(columns=columns_to_discard,inplace=True)
dataset["router"]=[1 if x[0] in ['p','s'] else 0 for x in dataset["sysname"].values]
dataset["switch"]=[1 if x[0] in ['a','k'] else 0 for x in dataset["sysname"].values]

for column in dataset.columns:  # Convert values to string or boolean
    unique_values = dataset[column].unique()
    if len(unique_values) == 2:
        unique_values.sort()
        if np.array_equal(unique_values, [0, 1]):
            dataset[column] = dataset[column].astype(bool)
    else:
        dataset[column] = dataset[column].astype(str)


# #convert columns_to_anonymize_deny_list to string format
# for column in columns_to_anonymize_deny_list:
#     dataset[column] = dataset[column].astype(str)

# anonymizer = PresidioReversibleAnonymizer(
#     analyzed_fields=[], # choose inbuilt fields to be considered for anonimyzation
#     faker_seed=42,
# )

# Define custom regex patterns to add in presidio for anonimyzation --> anonymized entries will be named 'support_entity_{occurence_no}'
# SYSTEM_NAME_pattern = Pattern(name="sysname_pattern", regex="[a-z]{4}[0-9]{3,4}", score=0.8)
# IC01_pattern = Pattern(name="ic01_pattern", regex="[0-9]{4,7}",score=1.0)
# IPV4_IP_pattern = Pattern("customer_name_alnum_pattern",regex="[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", score=0.8)

# anonymizer.add_recognizer(PatternRecognizer(supported_entity="SYSTEM_NAME_PLACEHOLDER", patterns=[SYSTEM_NAME_pattern]))
# anonymizer.add_recognizer(PatternRecognizer(supported_entity="IC01_PLACEHOLDER", patterns=[IC01_pattern]))
# anonymizer.add_recognizer(PatternRecognizer(supported_entity="sdwan_ip_admin_PLACEHOLDER", patterns=[IPV4_IP_pattern]))

# for column in columns_to_anonymize_deny_list:
#     anonymizer.add_recognizer(PatternRecognizer(supported_entity=f"{column}",
#                                                 deny_list=list(dataset[column].unique()),
#                                                 deny_list_score=0.5)) 



# save processed csv fie in parquet format
if "processed_data" not in os.listdir():
    os.mkdir("./processed_data")
dataset.to_parquet("processed_data/raw_data.parquet",index=False)



# make a dataset description file with unique features
feature_columns=["type_service","Service","TM Manager","country","region","Sales Country","Sales Region"] # Columns for which unique values need to be added in the description file

columns=dataset.columns
with open("temp/InfoChest.txt", "w+") as file:
    for column in columns:
        file.write(f"\nColumn name: {column}\n\nUnique Values:\n")
        if column in columns_to_anonymize:
            file.writelines(f"<{column}_placeholder>\n<{column}_placeholder_1>\n<{column}_placeholder_2>\nand more in similar fashion\n")
            file.write("\n")
        if column not in feature_columns:
            continue
        unique_values = dataset[column].unique()
        file.writelines(f"{value}\n" for value in unique_values)
        file.write("\n")