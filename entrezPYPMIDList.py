from Bio import Entrez
import os
import sys
import time

Entrez.email = 'lfabani@somalogic.com'  # Set your email address

def save_text_to_file(text, file_path):
    with open(file_path, 'w') as file:
        file.write(text)

def fetch_pubmed_articles(query):
    handle = Entrez.esearch(db='pubmed', term=query)
    record = Entrez.read(handle)
    handle.close()

    for pubmed_id in record['IdList']:
        pubmed_article = Entrez.efetch(db='pubmed', id=pubmed_id, rettype='medline', retmode='text')
        article_text = pubmed_article.read()
        pubmed_article.close()
      # Split the article text into lines
        lines = article_text.strip().split('\n')
        abstract_start = False
        abstract_lines = []
        for line in lines:
            if line.startswith('AB  - '):
                abstract_start = True
                abstract_lines.append(line.strip())
            elif line.startswith('      '):
                # Append abstract lines, removing leading spaces
                abstract_lines.append(line.strip())
            elif line and abstract_start:
                # End of abstract, break the loop
                break

        # Combine abstract lines into a single text
        abstract_text = '\n'.join(abstract_lines)

        # Generate file name
        file_name = f"{pubmed_id}.txt"
        file_path = os.path.join("DiscoveryTextFiles", file_name)

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File {file_name} already exists. Skipping...")
        else:
            # Save the article text to a file
            save_text_to_file(abstract_text, file_path)
            print(f"Saved file {file_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a list of PMIDs as arguments.")
    else:
        pmid_list = sys.argv[1:]
        for pmid in pmid_list:
            fetch_pubmed_articles(pmid)

