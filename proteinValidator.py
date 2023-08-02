import pickle
import pandas as pd
# Load the dictionary from the pickle file
file_path = "picklDir/allProteins.pickle"
with open(file_path, "rb") as file:
    loaded_dict = pickle.load(file)

excel_file_path = 'data/DataForReview.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Access the second column using the column name
second_column = df['Proteins'] 
first_column = df['File Name']
fileList = first_column.values.tolist()
proteinList = second_column.values.tolist()
questionProteins = {}
counter = 0
for protein in proteinList:
    proteinRow = protein.split(",")
    for proteins in proteinRow:
        isValid = False
        proteins = proteins.strip()
        for proteinNameList in loaded_dict.values():
            proteinNameList = [name.lower() for name in proteinNameList]
            if proteins.lower() in proteinNameList:
                isValid = True
        if isValid == False:
            if fileList[counter] not in questionProteins.keys():

                questionProteins[fileList[counter]]=proteins
            else:
                questionProteins[fileList[counter]]+= ","+proteins 
    counter += 1
print(questionProteins)            
with open("picklDir/questionableProt.pickle","wb") as qFile:
    pickle.dump(questionProteins,qFile)

