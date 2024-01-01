import os
from Bio import PDB

class PDBChainSplitter:
    """Class to split PDB files into separate chain files."""

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_files = set()  # Tracks processed files

    def process_pdb_files(self):
        # Scan output folder to avoid reprocessing files
        for pdb_file in os.scandir(self.output_folder):
            if pdb_file.is_file() and pdb_file.name.endswith(".pdb"):
                self.processed_files.add(pdb_file.name[:4])

        # Process files in the input folder
        for pdb_file in os.scandir(self.input_folder):
            if pdb_file.is_file() and pdb_file.name.endswith(".pdb"):
                base_filename = os.path.splitext(pdb_file.name)[0]
                if base_filename[:4] in self.processed_files:
                    print(f"Skipping {base_filename} as it's already processed.")
                    continue

                try:
                    self.split_pdb_chains(pdb_file.path)
                except Exception as e:
                    print(f"Error processing {pdb_file.path}: {e}")

    def split_pdb_chains(self, input_pdb_path):
        parser = PDB.PDBParser(QUIET=True)
        try:
            structure = parser.get_structure("protein", input_pdb_path)
        except Exception as e:
            print(f"Error parsing {input_pdb_path}: {e}")
            return

        for model in structure:
            chains = list(model)
            single_chain = len(chains) == 1

            for chain in chains:
                chain_id = chain.id
                base_filename = os.path.splitext(os.path.basename(input_pdb_path))[0]
                chain_output_path = os.path.join(self.output_folder, f"{base_filename}_{chain_id}.pdb")

                try:
                    io = PDB.PDBIO()
                    io.set_structure(chain)
                    io.save(chain_output_path)
                except Exception as e:
                    print(f"Error writing {chain_output_path}: {e}")

                if single_chain:
                    print(f"File {chain_output_path} only has 1 chain.")
                else:
                    print(f"Separated {chain_output_path}")

"""# Example usage
input_folder = "path/to/input"
output_folder = "path/to/output"
splitter = PDBChainSplitter(input_folder, output_folder)
splitter.process_pdb_files()
"""