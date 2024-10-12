from processing.load_data import DataLoader


def main():
    # Retrieve the data and save it in proper location (if not present)
    loader = DataLoader()
    loader.load_the_data()

if __name__ == "__main__":
    main()