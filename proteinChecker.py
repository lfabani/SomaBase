import pandas as pd

def check_proteins_exist(file_with_proteins, big_proteins_file):
    # Read the CSV files using pandas
    df_proteins = pd.read_excel(file_with_proteins)
    df_big_proteins = pd.read_csv(big_proteins_file,delimiter = ',')

    # Create a set of all proteins in the big proteins file for faster lookup
    all_big_proteins = set(df_big_proteins.values.flatten())
    print(all_big_proteins)
    # Function to check if proteins exist in the big proteins file
    def check_protein_existence(protein_list):
        proteins = protein_list.split(',')
        for protein in proteins:
            if protein.strip() not in all_big_proteins:
                print("found dat shit brinj")
                return True
        return False

    # Apply the check_protein_existence function to the proteins column in the first file
    df_proteins['Proteins'] = df_proteins['proteins'].apply(check_protein_existence)


if __name__ == "__main__":
    file_with_proteins_csv = "data/DataForReview.xlsx"
    big_proteins_file_csv = "data/output_1.csv"

    not_found_proteins_df = check_proteins_exist(file_with_proteins_csv, big_proteins_file_csv)
    print(not_found_proteins_df)

