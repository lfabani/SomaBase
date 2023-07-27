import subprocess
import csv
import pandas as pd
import easygui
import pickle
import os


def proteinConverter(protein_name, organism_name):
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


# Function to save the protein dictionary
def save_protein_dict(protein_dict, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(protein_dict, f)


# Function to load the protein dictionary
def load_protein_dict(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


data = pd.read_csv("data/PubsMasterQ1_23.csv", encoding='latin1', low_memory=False)
columns = data.loc[:, 'Biomarkers']
pd.set_option('display.max_rows', None)
proteinDict = load_protein_dict('protein_dict.pkl')  # Load the protein dictionary from file
beenUpdatedColls = data.loc[:, 'Been Converted']
index = 0

for proteinString in columns:
    if beenUpdatedColls[index] == 0:
        if type(proteinString) == str:
            ProteinList = proteinString.split(",")
            fullCell = ""

            for protein in ProteinList:
                if protein in ", ":
                    pass
                found_in_protein_file = False
                protein.strip()
                # Check if protein is already present in protein.tsv
                with open('protein.tsv', 'r') as f:
                    reader2 = csv.DictReader(f, delimiter='\t')
                    for row in reader2:
                        if row['Protein names'] is None:
                            pass
                        else:
                            if protein.lower() == row['Protein names'].lower():
                                found_in_protein_file = True
                                correctProtein = row['Entry']
                                break

                if found_in_protein_file:
                    # Protein is already in the protein file, no need for API call
                    pass
                else:
                    # Run the API call and append the new protein information to protein.tsv

                    if protein.lower() not in proteinDict.keys():
                        subprocess.run(["python", "extensiveFinder.py", protein, "Human"])
                        entry_values = proteinConverter(protein, "Human")

                        if len(entry_values) >= 1:
                            choices = []
                            for entry in entry_values:
                                protein_info = f"{entry[0]}, - {entry[1]}, - ({entry[2]})"
                                choices.append(protein_info)
                            choices.append("Type Another Option")
                            # Prompt the user to select the UniProt ID from the list or enter another option
                            choice = easygui.choicebox("Select the UniProt ID or choose 'Type Another Option':",
                                                       choices=choices,
                                                       title=f"This is the protein we are on: {protein}")
                            if choice == "Type Another Option":
                                # Prompt the user to manually enter an option
                                choice = easygui.enterbox("Enter the UniProt ID:")
                            correctProtein = choice.split(',')[0]
                        else:
                            choice = easygui.enterbox(title="Check to see if this is a valid protein name and enter "
                                                            "an ID of your choice:", msg=protein)
                            correctProtein = choice.split(',')[0]

                        proteinDict[protein.lower()] = correctProtein  # Update the protein dictionary
                    else:
                        correctProtein = proteinDict[protein.lower()]
                    save_protein_dict(proteinDict, 'protein_dict.pkl')

                    # Append new protein information to protein.tsv
                    with open('protein.tsv', 'a') as f:
                        writer = csv.writer(f, delimiter='\t')
                        writer.writerow([correctProtein, protein, "Human"])

                if " " in correctProtein:
                    correctProtein = correctProtein.split(" ")[0]
                fullCell += correctProtein + ","
            print(fullCell)
            data.loc[index, 'UNIProt ID'] = fullCell
            data.loc[index, 'Been Converted'] = 1
            # Save the protein dictionary to file

    index += 1  # Increment index after each iteration

data.to_csv("data/PubsMasterQ1_23.csv", index=False)
