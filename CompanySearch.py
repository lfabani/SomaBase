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

def ProteinCounterFunction(proteinString,proteinDict):
    counterList = []
    if isinstance(proteinString, str):
        for protein in proteinString.split(","):
            if protein not in ("     "):
                protein = protein.strip()
                if protein not in counterList:
                    counterList.append(protein)
                    if protein not in proteinDict.keys():
                        proteinDict[protein] = 1
                    else:
                        proteinDict[protein] += 1



if len(sys.argv) != 2:
    print("Usage: python script.py <Company_name>")
    sys.exit(1)
company_name = sys.argv[1]
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

for company in companyColumns:

    if company_name == company:
        ProteinCounterFunction(proteinColumns[indexer], proteinCounterDict)
    if checkerColumns[indexer] == 1:
        if isinstance(diseaseStateColumns[indexer], str):
            if diseaseStateColumns[indexer].strip() not in companyDict.keys():
                companyDict[diseaseStateColumns[indexer].strip()] = 1
                researchTopicProteinDict[diseaseStateColumns[indexer].strip()] = [proteinColumns[indexer]]  # Initialize as a list
            else:
                companyDict[diseaseStateColumns[indexer].strip()] += 1
                if isinstance(proteinColumns[indexer], str):
                    researchTopicProteinDict[diseaseStateColumns[indexer].strip()].append(proteinColumns[indexer])  # Append to the list



    indexer += 1


nickname_str = ""

#for key in proteinCounterDict.keys():
  #  output = subprocess.check_output(["python", "IndividualEntryFinder.py", key]).decode("utf-8").strip()
 #   nickname_str += output + "/"
#    nameDict[key] = output

# Create a DataFrame from the protein dictionary
df = pd.DataFrame(list(companyDict.keys()),columns=['Research Topic'])
df['Research Counter'] = df['Research Topic'].map(companyDict)
df['Research Proteins'] = df['Research Topic'].map(researchTopicProteinDict)
print(len(proteinCounterDict.keys()))
protein_df = pd.DataFrame(proteinCounterDict.items(), columns=['Protein Name', 'Protein Count'])
protein_df = protein_df.sort_values('Protein Count', ascending=False)
protein_df['Research Topic'] = df['Research Topic']
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Merge the protein_df DataFrame with the research topics DataFrame
merged_df = pd.merge(df, protein_df, how='outer', on='Research Topic')


# Save the merged DataFrame to an Excel file
merged_df.to_excel("data/CompanySpecificResults.xlsx", index=False)

