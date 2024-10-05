import pandas as pd
import os
import re


def main():
    # Store cleaned name for each pokemon 
    df = pd.read_csv('data/Pokedex_Ver_SV2.csv')
    df["Cleaned_Name"] = df["Original_Name"].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x.strip().lower()))

    # Getting the image names from the filenames 
    directory = "data/pokemon_images"
    image_names = [os.path.splitext(file)[0].strip().lower() for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    # Cycle through image names and map to df record containing corresponding pokemon information
    for image_name in image_names:
        cleaned_image_name = re.sub(r'[^A-Za-z0-9-]', '', image_name)
        matching_rows = df[df["Cleaned_Name"] == cleaned_image_name]
        if matching_rows.empty:
            matching_rows = df[df["Cleaned_Name"].str.contains(cleaned_image_name.split('-')[0], case=False)] 
        matching_indices = matching_rows.index.tolist()
        if matching_indices:
            for index in matching_indices:
                df.at[index, "Image_Name"] = f"{image_name}.png"
    
    empty_rows = df[df["Image_Name"].isna()]
    pokemon_with_no_images = empty_rows["Original_Name"].tolist()
    try:
        assert not pokemon_with_no_images
    except:
        raise AssertionError(f"Following pokemons exist that do not have a corresponding image: {', '.join(pokemon_with_no_images)}")



if __name__ == "__main__":
    main()