from src.processing.load_data import DataLoader


def main():
    # Retrieve the data and save it in proper location (if not present)
    DataLoader.load_the_data()

if __name__ == "__main__":
    main()