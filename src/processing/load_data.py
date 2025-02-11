import pandas as pd
import os
import re
from typing import List, Optional


class DataLoader:
    """
    A class to load and process Pokemon data from CSV and image files.

    Attributes:
        pokemon_info (Optional[pd.DataFrame]): DataFrame containing Pokemon information.
    """

    def __init__(self) -> None:
        """
        Initialize the DataLoader with an empty Pokemon information DataFrame.
        """
        self.pokemon_info: Optional[pd.DataFrame] = None

    def load_the_data(self, csv_path: str = 'data/Pokedex_Ver_SV2.csv', image_dir: str = 'data/pokemon_images') -> None:
        """
        Load Pokemon data from CSV file, clean names, and map images to Pokemon information.

        Args:
            csv_path (str): Path to the Pokemon CSV file.
            image_dir (str): Directory containing Pokemon images.

        Returns:
            pd.DataFrame: Processed Pokemon information DataFrame.

        Raises:
            FileNotFoundError: If CSV or image directory does not exist.
            AssertionError: If any Pokemon in the dataset lacks a corresponding image.
        """
        # Validate file paths
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        if not os.path.exists(image_dir):
            raise FileNotFoundError(f"Image directory not found: {image_dir}")
            
        # Store cleaned name for each pokemon 
        self.pokemon_info = pd.read_csv('data/Pokedex_Ver_SV2.csv')
        self.pokemon_info["Cleaned_Name"] = self.pokemon_info["Original_Name"].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x.strip().lower()))

        # Getting the image names from the filenames 
        image_names = self.get_image_names("data/pokemon_images")

        # Cycle through image names and map to df record containing corresponding pokemon information
        self.pokemon_info = self.map_images_to_info(image_names)
    
    @staticmethod
    def _get_image_names(directory: str) -> List[str]:
        """
        Retrieve a list of image filenames from the specified directory.

        Args:
            directory (str): Path to the directory containing image files.

        Returns:
            List[str]: List of image filenames without extensions, converted to lowercase.
        """
        return [os.path.splitext(file)[0].strip().lower() for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    def _map_images_to_info(self, image_names: List[str]) -> pd.DataFrame:
        """
        Map image names to corresponding Pokemon information in the DataFrame.

        Args:
            image_names (List[str]): List of image names to match against Pokemon names.

        Returns:
            pd.DataFrame: Updated DataFrame with image names added.

        Raises:
            AssertionError: If any Pokemon lacks a corresponding image.
        """
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