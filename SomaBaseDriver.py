import easygui
import subprocess
import pickle
import os


def load_pickle_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return []


while True:
    choices = ["Search", "Update DataBase", "View Total Protein Count"]
    choice = easygui.choicebox("Please select the type of interaction you would like to have.",
                               choices=choices,
                               title="SomaBase")
    if choice is None:
        break
    if choice == "Search":
        searchChoices = ["Search by Company", "Search by Protein", "Search by Research Topic"]
        searchChoice = easygui.choicebox("Please select the type of search you would like to have.",
                                         choices=searchChoices,
                                         title="SomaBase")
        if searchChoice == "Search by Company":
            CompanyName = easygui.enterbox("Enter the name of the company you would like to search for.",
                                           title="SomaBase")
            subprocess.run(["python", "CompanySearch.py", CompanyName])
        elif searchChoice == "Search by Protein":
            ProteinName = easygui.enterbox("Enter the name/uniprot id of the protein you want to search for.",
                                           title="SomaBase")
            isUniprot = easygui.enterbox("If the ID you typed is the protein's UniProt ID, type 0, otherwise type 1.",
                                         title="SomaBase")
            subprocess.run(["python", "IndividualProteinSearch.py", ProteinName, isUniprot])
        elif searchChoice == "Search by Research Topic":
            subprocess.run(["python", "ResearchTopicGathering.py"])
            ResearchChoices = load_pickle_list("researchTopics.pkl")
            ResearchChoices.append("type another research name")
            researchTopicName = easygui.choicebox("Enter the type of research Topic you are looking for.",
                                                  choices=ResearchChoices, title="SomaBase")
            if researchTopicName == 'type another research name':
                researchTopicName = easygui.enterbox(title="Type the research topic of your choice")
            subprocess.run(["python", 'ResearchTopic.py', researchTopicName])
    elif choice == "Update DataBase":
        pmid = easygui.enterbox("Enter the PMID of interest")

    elif choice == "View Total Protein Count":
        subprocess.run(["python", "DataBaseResults.py"])
