import pickle
import pandas as pd

# Load the pickle dictionary
with open("picklDir/NLPProteinDict.pickle", "rb") as file:
    pickle_dict = pickle.load(file)

# Initialize a list to store rows of data
rows = []

# Iterate through the dictionary and create rows for each file
for file_name, proteins in pickle_dict.items():
    proteinsList = []
    for protein in proteins:
        if protein not in "!, ":
            protein = protein.replace('(','')
            protein = protein.replace(')','')
            protein = protein.strip(",")
            proteinsList.append(protein)
    with open(f"picklDir/label_to_category_{file_name}.pickle","rb") as catFile:
        categoryDict = pickle.load(catFile)
#        print(categoryDict)
    row = [file_name, ", ".join(proteinsList)]  # Join all proteins into a single string
    for genCat,subCat in categoryDict.items():
        row.append(genCat)
        string = ""
        for sub in subCat:
            string+=sub
        row.append(string)
    print(row)
    rows.append(row)
    
# Create a DataFrame from the list of rows
df = pd.DataFrame(rows, columns=["File Name", "Proteins","General Topic","Subtopic","Secondary General Topic","Secondary Subtopic"])

# Write the DataFrame to an Excel file
output_file = "data/DataForReview.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been saved to {output_file}")

