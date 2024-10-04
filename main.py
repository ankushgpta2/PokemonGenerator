import pandas as pd
import re


def main():
    # Store cleaned name for each pokemon 
    df = pd.read_csv('data/Pokedex_Ver_SV2.csv')
    df["Cleaned_Name"] = df["Original_Name"].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x.strip().lower()))

    # Getting the image names from the filenames 
    directory = "data/pokemon_images"
    image_names = [os.path.splitext(file)[0].strip().lower() for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


if __name__ == "__main__":
    main()