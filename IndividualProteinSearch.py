import easygui
import pandas as pd
import sys
import os
import pickle
import subprocess
import csv


def load_protein_dict(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def proteinConverter(protein_name):
    proteinNames = []
    listForTrackingRepeats = []
    with open('protein.tsv', 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['Protein names'] is None:
                pass
            else:
                if protein_name.lower() in row['Protein names'].lower().replace(",", "") or \
                        protein_name.lower() in row['Gene Names'].lower().replace(",", ""):
                    if row['Entry'] not in listForTrackingRepeats:
                        proteinNames.append((row['Entry'], row['Protein names'], row['Gene Names']))
                        listForTrackingRepeats.append(row['Entry'])

    return proteinNames


if len(sys.argv) != 3:
    print("Usage: python script.py <Protein Name> <IsUNIProt>")
    sys.exit(1)
protein_name = sys.argv[1]
isUniProt = sys.argv[2]
if isUniProt == '1':
    subprocess.run(["python", "extensiveFinder.py", protein_name, "Human"])
    potentialNames = proteinConverter(protein_name)
    if len(potentialNames) >= 1:
        choices = []
        for entry in potentialNames:
            protein_info = f"{entry[0]}, - {entry[1]}, - ({entry[2]})"
            choices.append(protein_info)
        choices.append("Type Another Option")
        # Prompt the user to select the UniProt ID from the list or enter another option
        choice = easygui.choicebox("Select the UniProt ID or choose 'Type Another Option':",
                                   choices=choices,
                                   title=f"This is the protein we are on: {protein_name}")
        protein_name = choice.split(',')[0]

data = pd.read_csv("data/PubsMasterQ1_23.csv", encoding='latin1', low_memory=False)
proteinColumns = data.loc[:, 'UNIProt ID']
companyColumns = data.loc[:, 'Company']
diseaseStateColumns = data.loc[:, 'Research Topic']
indexer = 0
companyDict = {}
proteinCounterDict = {}
researchTopicDict = {}
nameDict = {}
RelatedProteinsDict = {}
for protein in proteinColumns:
    if isinstance(protein, str):
        if protein_name in protein:
            for proteins in protein.split(","):
                # finding related proteins
                if proteins == "" or protein_name in proteins:
                    pass
                else:
                    if proteins not in RelatedProteinsDict:
                        RelatedProteinsDict[proteins] = 1
                    else:
                        RelatedProteinsDict[proteins] += 1
            # finding a count by company name
            if companyColumns[indexer].strip() not in companyDict.keys():
                companyDict[companyColumns[indexer].strip()] = 1
            else:
                companyDict[companyColumns[indexer].strip()] += 1
            # finding count by research topic
            if diseaseStateColumns[indexer].strip() not in researchTopicDict.keys():
                researchTopicDict[diseaseStateColumns[indexer].strip()] = 1
            else:
                researchTopicDict[diseaseStateColumns[indexer].strip()] += 1

    indexer += 1

nickname_str = ""

# Create a DataFrame from the protein dictionary
df = pd.DataFrame(list(companyDict.keys()), columns=['Company Name'])
df['Company Counter'] = df['Company Name'].map(companyDict)
protein_df = pd.DataFrame(RelatedProteinsDict.items(), columns=['Related Proteins', 'Protein Count'])
df['Related Proteins'] = protein_df['Related Proteins']
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Merge the protein_df DataFrame with the research topics DataFrame
temp_merged_df = pd.merge(df, protein_df, how='outer', on='Related Proteins')
researchTopicDf = pd.DataFrame(researchTopicDict.items(), columns=['Research Topic', 'Topic Count'])
researchTopicDf['Related Proteins'] = temp_merged_df['Related Proteins']
merged_df = pd.merge(temp_merged_df, researchTopicDf, how='outer', on='Related Proteins')

# Save the merged DataFrame to an Excel file
merged_df.to_excel("data/SpecificProteinResults.xlsx", index=False)