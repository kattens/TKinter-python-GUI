import os
import requests
import csv

class PDBDownloader:
    """
    This class is designed to download PDB files.
    It takes a directory to save the downloaded files and a list of protein names.
    The protein names can be provided as either a Python list or a CSV file with names in a column.
    """

    def __init__(self, directory, protein_names):
        """
        Initialize the downloader with the output directory and protein names.
        If protein_names is a string, it's treated as a path to a CSV file.
        If it's a list, it's used directly.
        """
        self.directory = directory

        # Create the directory if it does not exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Handle different types of protein_names input
        if isinstance(protein_names, str):
            self.protein_names = self.read_from_csv(protein_names)
        elif isinstance(protein_names, list):
            self.protein_names = protein_names
        else:
            raise ValueError("protein_names must be a list or a path to a CSV file")
            
    def read_from_csv(self, file_path):
        """
        Read protein names from a CSV file.
        Assumes the names are in the first column.
        """
        try:
            with open(file_path, 'r') as csv_input:
                return [row[0] for row in csv.reader(csv_input)][1:]
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at {file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")

    def download_pdb(self):  
        """
        Download PDB files for each protein name in the list.
        Skips download if the file already exists.
        """
        for protein_name in self.protein_names:
            filename = f"{protein_name}.pdb"
            file_path = os.path.join(self.directory, filename)

            if os.path.exists(file_path):
                print(f"File already exists for {protein_name}, skipping download.")
                continue

            url = f"https://files.rcsb.org/download/{protein_name}.pdb"
            try:
                response = requests.get(url)
                response.raise_for_status()

                if "HEADER    " not in response.text:
                    print(f"No PDB file found for {protein_name}")
                    continue

                with open(file_path, "w") as file:
                    file.write(response.text)
                print(f"Downloaded PDB file for {protein_name} to {self.directory}")
            except requests.HTTPError as e:
                print(f"Failed to download PDB file for {protein_name}: HTTP Error {e}")
            except Exception as e:
                print(f"Failed to download PDB file for {protein_name}: Error {e}")

# Example Usage:
# downloader = PDBDownloader("path/to/directory", "path/to/csvfile.csv")
# downloader = PDBDownloader("path/to/directory", ["protein1", "protein2"])
# downloader.download_pdb()
