import argparse
import os
import pandas as pd

def remove_strings_from_second_row(filename,strings_to_remove):
    excel_file_path = os.path.join("data", "DataForReview.xlsx")
    
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)
    first_col = df['File Name'].values.tolist()
    correctIndex = 0
    print(f"the filename is {filename}")
    for file in first_col:
        print(file)
        if filename in file:
            break
        correctIndex += 1
    # Get the second row as a list
    second_col = df['Proteins'].values.tolist()
    print(second_col[correctIndex])
    # Remove the specified strings from the second row
    for string in strings_to_remove: 
        if string in second_col[correctIndex]:
            second_col[correctIndex]=second_col[correctIndex].replace(string,"")
            print(f"removed {second_col[correctIndex]}")
    # Update the DataFrame with the modified second row
    df['Proteins'] = second_col

    # Save the updated DataFrame back to the Excel file
    df.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove strings from the second row of the default Excel file (DataForReview.xlsx).")
    parser.add_argument("filename",help = "filename that we are looking at to remove")
    parser.add_argument("strings_to_remove", nargs="+", help="List of strings to remove from the second row")

    args = parser.parse_args()
    filename = args.filename
    strings_to_remove = args.strings_to_remove

    remove_strings_from_second_row(filename,strings_to_remove)

    print("Strings removed successfully from the second row of the Excel file.")

