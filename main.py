import pandas as pd
import re


# store cleaned name for each pokemon 
df = pd.read_csv('data/Pokedex_Ver_SV2.csv')
df["Cleaned_Name"] = df["Original_Name"].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x.strip().lower()))
