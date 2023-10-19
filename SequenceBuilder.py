#extract the sequences: similar to the phase 1
import csv
from Bio import PDB 
import os
import csv
import pandas as pd

class SequenceBuilder:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def extract_sequence_from_pdb(self, file_path):
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("temp", file_path)z
        model = structure[0]
        seq = ""

        for chain in model:
            for residue in chain:
                if PDB.is_aa(residue):
                    try:
                        seq += PDB.Polypeptide.three_to_one(residue.get_resname())
                    except KeyError:
                        seq += 'X'  # For unknown residues, use 'X' as a placeholder
                else:
                    seq += 'X'  # For non-amino acid residues, use 'X' as a placeholder
        return seq

    def sequence_builder(self):
        sequences = {}
        data = []

        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path) and file_path.lower().endswith('.pdb'):  # Only process PDB files
                sequence_name = os.path.splitext(filename)[0]  # Use filename (without extension) as sequence name
                sequence = self.extract_sequence_from_pdb(file_path)
                sequences[sequence_name] = [sequence, filename]

        # Build a DataFrame
        for key, value in sequences.items():
            data.append([key, value[0]])
        df = pd.DataFrame(data, columns=['seq name', 'seq'])
        return df
