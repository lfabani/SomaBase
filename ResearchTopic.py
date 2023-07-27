import subprocess
import pandas as pd
import sys
import os
import pickle


def load_protein_dict(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def ProteinAdder(ProteinString, CompanyProteinString):
    checker = False
    print(ProteinString)
    print("--------------------------------------------------------")
    print(CompanyProteinString)
    print("*********************************************************")
    for protein in ProteinString.split(","):
        print(f"we are looking at {protein}")
        if protein not in CompanyProteinString.split(",") and protein not in "      ":
            print("it wasn't there, adding now!")
            CompanyProteinString += protein + ","
    return CompanyProteinString


def ProteinCounterFunction(proteinString, proteinDict):
    counterList = []
    if isinstance(proteinString, str):
        for protein in proteinString.split(","):
            if protein not in "     ":
                protein = protein.strip()
                if protein not in counterList:
                    counterList.append(protein)
                    if protein not in proteinDict.keys():
                        proteinDict[protein] = 1
                    else:
                        proteinDict[protein] += 1


if len(sys.argv) != 2:
    print("Usage: python script.py <Research Topic>")
    sys.exit(1)
topic_name = sys.argv[1].lower()
data = pd.read_csv("data/PubsMasterQ1_23.csv", encoding='latin1', low_memory=False)
proteinColumns = data.loc[:, 'UNIProt ID']
companyColumns = data.loc[:, 'Company']
checkerColumns = data.loc[:, 'Been Converted']
diseaseStateColumns = data.loc[:, 'Research Topic']
indexer = 0
companyDict = {}
researchTopicProteinDict = {}
proteinCounterDict = {}
nameDict = {}

for topic in diseaseStateColumns:
    if isinstance(topic, str):
        if topic_name in topic.lower():
            ProteinCounterFunction(proteinColumns[indexer], proteinCounterDict)
            if checkerColumns[indexer] == 1:
                if isinstance(companyColumns[indexer], str):
                    if companyColumns[indexer].strip() not in companyDict.keys():
                        researchTopicProteinDict[companyColumns[indexer].strip()] = 1
                        companyDict[companyColumns[indexer].strip()] = proteinColumns[indexer]  # Initialize as a list
                    else:
                        researchTopicProteinDict[companyColumns[indexer].strip()] += 1
                        if isinstance(proteinColumns[indexer], str):
                            print(f"company iss {companyColumns[indexer]}")
                            companyDict[companyColumns[indexer].strip()] = ProteinAdder(proteinColumns[indexer],
                                                                                        companyDict[companyColumns[
                                                                                            indexer].strip()])

    indexer += 1

for key in proteinCounterDict.keys():
    output = subprocess.check_output(["python", "IndividualEntryFinder.py", key]).decode("utf-8").strip()
    nameDict[key] = output

print(nameDict)
# Create a DataFrame from the protein dictionary
df = pd.DataFrame(list(companyDict.keys()), columns=['Company Name'])
df['Company Count'] = df['Company Name'].map(researchTopicProteinDict)
df['Company Specific Proteins'] = df['Company Name'].map(companyDict)
protein_df = pd.DataFrame(proteinCounterDict.items(), columns=['Protein ID', 'Protein Count'])
protein_df2 = pd.DataFrame(nameDict.items(), columns=['Protein ID', 'Protein names'])
protein_df['Company Name'] = df['Company Name']
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(protein_df2)
# Merge the protein_df DataFrame with the research topics DataFrame
merged_df = pd.merge(df, protein_df, how='outer', on='Company Name')
print(
    "------------------------------------------------------------------------------------"
    "------------------------------")
merged_df2 = pd.merge(merged_df, protein_df2, how='outer', on='Protein ID')
print(merged_df2)
# Save the merged DataFrame to an Excel file
merged_df2.to_excel("data/TopicSpecificResults.xlsx", index=False)
