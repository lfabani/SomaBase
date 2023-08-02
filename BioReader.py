from transformers import BertTokenizer, BertForTokenClassification
import torch
import os
import pickle

def isMoreI(NerList,index):
    SecondName=''
    for i,(word,label) in enumerate(NerList):
        if (i > index and i < index + 3):
            if label == 'B':
                break
            elif label =='I':
               SecondName += word.strip('#')
    return SecondName

# Load the pre-trained model and tokenizer
model_path = "outputs/models/BENT-PubMedBERT-NER-Gene"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForTokenClassification.from_pretrained(model_path)
file_list = os.listdir("DiscoveryTextFiles")

        # Initialize an empty list to store all ProteinList from each file
all_protein_dict = {}

for file_name in file_list:
            # Check if the file is a text file (you may want to adjust this check based on your file names)
    if file_name.endswith(".txt"):
        file_path = os.path.join("DiscoveryTextFiles", file_name)
        with open(file_path,'r') as file:
            samples = file.read()
           # print(samples)
            max_chunk_length = 500  # Define the maximum chunk length

            ProteinList = []
            chunks = []
            start = 0

            while start < len(samples):
     # Find the nearest period to the chunk limit
                end = min(start + max_chunk_length, len(samples))
                nearest_period = samples.rfind('.', start, end)  # Find the last period within the chunk limit

                if nearest_period != -1 and nearest_period != start:
        # If a period was found within the chunk limit and it's not the first character of the chunk
                    chunk = samples[start:nearest_period + 1]  # Include the period in the chunk
                    start = nearest_period + 1  # Move the start position to after the period
                else:
        # If no period was found within the chunk limit or it's the first character of the chunk
                    chunk = samples[start:end]
                    start = end
                chunks.append(chunk)
        for text in chunks:
            text=text.replace('/',' / ')
# Define the text for NER prediction
            print(text)
# Tokenize the input text and convert it into model input format
            tokens = tokenizer.encode(text, add_special_tokens=True, return_tensors="pt")

# Perform NER prediction
            with torch.no_grad():
                model_output = model(tokens)[0]

# Decode the model output to get the predicted labels for each token
            predicted_label_ids = torch.argmax(model_output, dim=2)[0]

# Get the label-to-id mapping from the model's configuration
            label_map = model.config.id2label

# Convert label IDs back to human-readable labels
            predicted_labels = [label_map[label_id.item()] for label_id in predicted_label_ids]

# Convert tokens back to human-readable words
            words = tokenizer.convert_ids_to_tokens(tokens[0])
            ner_result = list(zip(words, predicted_labels))
          #  print(ner_result)
            proteins_list = []
            current_protein = None
            ProteinName = None
            continuing_protein = None
            last_2_chars = "N%"
            startedSecond = False
            index_array = []
            lastFlag = ''
            for i, (word, label) in enumerate(ner_result):
                count = 0
                HasFound = False
                ProteinStart = 0
                endOfProtein = 0
                start_count = -1
                if label == "B":
                    startedSecond= False
                    lastFlag = 'b'
                    if current_protein:
                        current_protein += word.strip("#")
                    else:
                        current_protein = word.strip("#")
                elif label == "I":
                    lastFlag = 'i'
                    if continuing_protein:
                        if '-' in word:
                            continuing_protein += word.strip("#")
                        else:
                            continuing_protein += " " + word.strip("#")
                    else:
                        continuing_protein = word.strip("#")
                        startedSecond = True
                elif label =='O' and word!='-':
                    if lastFlag == 'i' or lastFlag == 'b':
                        if continuing_protein: continuing_protein += isMoreI(ner_result,i)
                        lastFlag = 'o'
                #d current protein in orignial text and to avoid formatting
                        if current_protein:
                            if startedSecond and startedSecond == True:
                                for names in text.split():
                                    names = names.strip(",")
                                    names = names.strip("(")
                                    names = names.strip(")")
                                    start_count+=1
                                    if len(continuing_protein)>2:
                                        last_2_chars = continuing_protein[-2:]
                                    else:
                                        last_2_chars = continuing_protein[-1:]
                                    last_2_chars = last_2_chars.strip(" ")
                                    if current_protein.lower().replace('-',"") in names.lower().replace('-',"") and start_count not in index_array:
                                        ProteinStart = start_count
                                        HasFound=True
                                    if last_2_chars.lower() in names[-len(last_2_chars):].lower() and start_count not in index_array and HasFound == True:
                                        endOfProtein = start_count
                                        ProteinName = ""

                                        break
                                ProteinName = ""
                                for i,names in enumerate(text.split()):
                                    if i >= ProteinStart and i <= endOfProtein:
                                       ProteinName += names+ " "
                                index_array.append(ProteinStart)
                                index_array.append(endOfProtein)
                            if ProteinName==None:
                                 ProteinName = current_protein
                    current_protein = None
                    continuing_protein = None
                    if ProteinName:
                        ProteinName = ProteinName.strip()
                        ProteinName = ProteinName.strip("-")
                        ProteinName = ProteinName.strip(")")
                        ProteinName = ProteinName.strip("(")
                    if ProteinName not in ProteinList and ProteinName != None and ProteinName != "" and len(ProteinName)>2:
                        ProteinList.append(ProteinName)
                        print(ProteinList)
                    ProteinName = None
                else:
                    if lastFlag =='b':
                        current_protein+="-"
                    elif lastFlag =='i':
                        continuing_protein +="-"
            print(ProteinList)
        all_protein_dict[file_name]=ProteinList
        with open(f"picklDir/NLPProteinDict.pickle", "wb") as file:
            pickle.dump(all_protein_dict, file)

        print("ProteinList saved as ProteinDict.pickle")

