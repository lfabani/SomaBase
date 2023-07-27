import pandas as pd
import pickle
import os
def load_pickle_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        return []
def save_pickle_list(pickleList, file_path,existing_list):
    updated_list = existing_list + pickleList
    with open(file_path, 'wb') as f:
        pickle.dump(updated_list, f)


def get_column_values(csv_filename, column_name):
    df = pd.read_csv(csv_filename,encoding='latin1', low_memory=False)
    column_values = df[column_name].astype(str).str.strip().unique().tolist()
    column_values.sort()
    return column_values
csv_filename = 'data\PubsMasterQ1_23.csv'  # Replace with the actual CSV filename
column_name = 'Research Topic'  # Replace with the actual column name

column_values = get_column_values(csv_filename, column_name)

pickle_filename = 'researchTopics.pkl'  # Specify the pickle file name
pickleList = load_pickle_list(pickle_filename)
tempList = []
for item in column_values:
    if item not in pickleList and item != "":
        tempList.append(item)


save_pickle_list(tempList,pickle_filename,pickleList)