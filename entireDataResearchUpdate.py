import pandas as pd
import pickle
df = pd.read_CSV("data/PubsMasterQ1_23.csv")
ResearchCol = df['PMID'].values.tolist()
for pmid in ResearchCol:
    subprocess.run(['python3',"entrezPYMIDList.py",pmid])

subprocess.run(['python3',"bioGenreReader.py"])

