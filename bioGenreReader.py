import os
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from collections import Counter
import pandas as pd
# Define the model name or path for the rjac/biobert-ICD10-L3 model
model_name_or_path = "outputs/models/biobert-ICD10-L3"

# Load the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# Get the classification labels
labels = model.config.id2label

# Initialize an empty Counter to store the occurrences of each label
label_counter = Counter()

# Function to classify a text and update the label_counter
def classify_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label_id = logits.argmax(dim=1).item()
    predicted_label_name = labels[predicted_label_id]
    label_counter[predicted_label_name] += 1

# Process each file in the directory
file_list = os.listdir("DiscoveryTextFiles")
for file_name in file_list:
    # Check if the file is a text file (you may want to adjust this check based on your file names)
    if file_name.endswith(".txt"):
        file_path = os.path.join("DiscoveryTextFiles", file_name)
        with open(file_path, 'r') as file:
            samples = file.read()
            max_chunk_length = 500  # Define the maximum chunk length

            # Split the file content into chunks
            chunks = []
            start = 0
            while start < len(samples):
                end = min(start + max_chunk_length, len(samples))
                nearest_period = samples.rfind('.', start, end)
                if nearest_period != -1 and nearest_period != start:
                    chunk = samples[start:nearest_period + 1]
                    start = nearest_period + 1
                else:
                    chunk = samples[start:end]
                    start = end
                chunks.append(chunk)

            # Classify each chunk and update the label_counter
            for chunk in chunks:
                chunk = chunk.replace('/', ' / ')
                classify_text(chunk)

# Find the two most common labels
            most_common_labels = label_counter.most_common(2)
            categories_df = pd.read_csv("data/categories.csv")
            label_to_category_dict = {}
# Print the results
            for label, count in most_common_labels:
                for column in categories_df:                    
                    categories_df[column] = categories_df[column].astype(str)
                    labelFixed = label.split(" (")[0]
                    for row in categories_df[column]:
                        if labelFixed in row:
                            general_category = column
                            if general_category not in label_to_category_dict.keys():
                                label_to_category_dict[general_category] = [labelFixed]
                            else:
                                label_to_category_dict[general_category].append(labelFixed) 
                            break
            with open(f"picklDir/label_to_category_{file_name}.pickle", "wb") as f:
                pickle.dump(label_to_category_dict, f)
