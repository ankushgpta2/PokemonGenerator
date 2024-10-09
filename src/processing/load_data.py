import pandas as pd
import os
import re


class DataLoader:
    def __init__(self):
        self.pokemon_info = None

    def load_the_data(self):
        # Store cleaned name for each pokemon 
        self.pokemon_info = pd.read_csv('data/Pokedex_Ver_SV2.csv')
        self.pokemon_info["Cleaned_Name"] = self.pokemon_info["Original_Name"].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x.strip().lower()))

        # Getting the image names from the filenames 
        image_names = self.get_image_names("data/pokemon_images")

        # Cycle through image names and map to df record containing corresponding pokemon information
        self.pokemon_info = self.map_images_to_info(image_names)
    
    @staticmethod
    def _get_image_names(directory):
        return [os.path.splitext(file)[0].strip().lower() for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    def _map_images_to_info(self, image_names):
        for image_name in image_names:
            cleaned_image_name = re.sub(r'[^A-Za-z0-9-]', '', image_name)
            matching_rows = self.pokemon_info[self.pokemon_info["Cleaned_Name"] == cleaned_image_name]
            if matching_rows.empty:
                matching_rows = self.pokemon_info[self.pokemon_info["Cleaned_Name"].str.contains(cleaned_image_name.split('-')[0], case=False)] 
            matching_indices = matching_rows.index.tolist()
            if matching_indices:
                for index in matching_indices:
                    self.pokemon_info.at[index, "Image_Name"] = f"{image_name}.png"
        
        # Check if all pokemon have corresponding image 
        empty_rows = self.pokemon_info[self.pokemon_info["Image_Name"].isna()]
        pokemon_with_no_images = empty_rows["Original_Name"].tolist()
        try:
            assert not pokemon_with_no_images
        except:
            raise AssertionError(f"Following pokemons exist that do not have a corresponding image: {', '.join(pokemon_with_no_images)}")