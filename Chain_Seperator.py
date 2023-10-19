import os
import requests
import csv
from Bio import PDB  # Import the Bio.PDB module

class PDBChainSplitter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_files = set()

    def process_pdb_files(self):
        for pdb_file in os.scandir(self.output_folder):
            if pdb_file.is_file() and pdb_file.name.startswith("4") and pdb_file.name.endswith(".pdb"):
                self.processed_files.add(pdb_file.name[:4])

        for pdb_file in os.scandir(self.input_folder):
            if pdb_file.is_file() and pdb_file.name.endswith(".pdb"):
                base_filename = os.path.splitext(pdb_file.name)[0]
                if base_filename[:4] in self.processed_files:
                    print(f"Skipping {base_filename} as it's already processed.")
                    continue

                self.split_pdb_chains(pdb_file.path)

    def split_pdb_chains(self, input_pdb_path):
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("protein", input_pdb_path)

        for model in structure:
            chains = list(model)

            for chain in chains:
                chain_id = chain.id
                base_filename = os.path.splitext(os.path.basename(input_pdb_path))[0]
                chain_output_path = os.path.join(self.output_folder, f"{base_filename}_{chain_id}.pdb")

                io = PDB.PDBIO()
                io.set_structure(chain)
                io.save(chain_output_path)

                if len(chains) == 1:
                    print(f"File {chain_output_path} only has 1 chain.")
                else:
                    print(f"Separated {chain_output_path}")
