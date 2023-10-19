import os
import requests
import csv
from Bio import PDB  # Import the Bio.PDB module

# Define the PDBDownloader class with an output directory parameter
class PDBDownloader:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def download_pdb(self, protein_name_list):
        for protein_name in protein_name_list:
            filename = f"{protein_name}.pdb"
            file_path = os.path.join(self.output_directory, filename)

            # Check if the file already exists in the output directory
            if os.path.exists(file_path):
                print(f"File already exists for {protein_name}, skipping download.")
                continue

            url = f"https://files.rcsb.org/download/{protein_name}.pdb"

            try:
                response = requests.get(url)
                response.raise_for_status()
                pdb_content = response.text

                # Check if the response contains the PDB content
                if "HEADER    " not in pdb_content:
                    print(f"No PDB file found for {protein_name}")
                    continue

                with open(file_path, "w") as file:
                    file.write(pdb_content)

                print(f"Downloaded PDB file for {protein_name} to {self.output_directory}")
            except requests.HTTPError as e:
                print(f"Failed to download PDB file for {protein_name}")
                print(f"HTTP Error: {e}")
            except Exception as e:
                print(f"Failed to download PDB file for {protein_name}")
                print(f"Error: {e}")
