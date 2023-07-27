import os
import pickle
import subprocess
import sys
import pandas as pd

def load_protein_dict(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

data = pd.read_csv("data/PubsMasterQ1_23.csv", encoding='latin1', low_memory=False)
columns = data.loc[:, 'UNIProt ID']
ProteinDict = {}
nameDict = {}

#output = subprocess.check_output(["python", "IndividualEntryFinder.py", "B7Z2I6"]).decode("utf-8").strip()

# Count the occurrences of each protein
for proteins in columns:
    counterList = []
    if isinstance(proteins, str):
        for protein in proteins.split(","):
            if protein not in ("     "):
                protein = protein.strip()
                if protein not in counterList:
                    counterList.append(protein)
                    if protein not in ProteinDict.keys():
                        ProteinDict[protein] = 1
                    else:
                        ProteinDict[protein] += 1

nickname_str = ""

for key in ProteinDict.keys():
    output = subprocess.check_output(["python", "IndividualEntryFinder.py", key]).decode("utf-8").strip()
    nickname_str += output + "/"
    nameDict[key] = output

# Create a DataFrame from the protein dictionary
df = pd.DataFrame(list(ProteinDict.items()), columns=['Protein Name', 'Count'])
df['Protein Nicknames'] = df['Protein Name'].map(nameDict)

# Sort the DataFrame by count in descending order
df = df.sort_values('Count', ascending=False)

# Save the DataFrame to an Excel file
df.to_excel("data/protein_counts.xlsx", index=False)