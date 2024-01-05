import os
import json
import csv
from Bio import PDB
from Bio.PDB.Polypeptide import is_aa  # Make sure to import this if it's not already

class PDBProcessor:
    def __init__(self, folder_path,methods_to_call):
        def __init__(self, folder_path, methods_to_call):
            self.folder_path = folder_path
            self.methods_to_call = methods_to_call  # List of methods to call
            self.all_protein_data = []  # Initialize the list to hold all protein data.
            self.process_all_pdb_files()

    def process_all_pdb_files(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".pdb"):
                self.current_filename = filename[:-4]  # Save the current file name without extension
                file_path = os.path.join(self.folder_path, filename)
                print(f"Processing {filename}")
                try:
                    with open(file_path, 'r') as f:
                        self.pdb_lines = f.readlines()
                    self.structure = PDB.PDBParser(QUIET=True).get_structure('PDB', file_path)
                    self.all_protein_data.append(self.get_pdb_info())
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")
                    
        self.write_data_to_json()
        self.write_data_to_csv()

    def get_pdb_info(self):
        protein_data = {}
        method_functions = {
            "Protein Name": self.protein_name,
            "Polymer Entity": self.polymer_entity,
            "Sequence": self.sequence,
            "C-alpha Coordinates": self.c_alpha_coords,
            "Refinement Resolution": self.refinement_resolution,
            "Experiment Type": self.experiment_type,
            "Enzyme Classification": self.enzyme_classification,
            "Symmetry Type": self.symmetry_type,
            "R Factor": self.r_factor,
            "B Factor": self.b_factor
        }

        for method_name in self.methods_to_call:
            if method_name in method_functions:
                protein_data[method_name] = method_functions[method_name]()

        return protein_data
    
    
    def write_data_to_json(self):
        
        with open('PDBFiles.json', 'w') as json_file:
            json.dump(self.all_protein_data, json_file, indent=4)
        print("Data has been written to PDBFiles.json")

    def write_data_to_csv(self):

        # Define the header(name of the columns) based on the keys of the first protein data
        header = self.all_protein_data[0].keys()

        with open('PDBFiles.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for protein_data in self.all_protein_data:
                writer.writerow(protein_data)

        print("Data has been written to PDBFiles.csv")


    def protein_name(self):
        # Return the filename without the .pdb extension
        return self.current_filename


    def polymer_entity(self):
        criteria = {"DNA": False, "Protein": False, "RNA": False}
        for model in self.structure:
            for chain in model:
                for residue in chain:
                    if residue.resname in ["DA", "DT", "DC", "DG"]:
                        criteria["DNA"] = True
                    elif residue.resname in ["A", "U", "C", "G"]:
                        criteria["RNA"] = True
                    elif is_aa(residue, standard=True):
                        criteria["Protein"] = True
        return ('DNA' if criteria["DNA"] else '') + \
               ('RNA' if criteria["RNA"] else '') + \
               ('Protein' if criteria["Protein"] else '') or 'Unknown'

    def sequence(self):
        sequences = {'Protein': [], 'DNA': [], 'RNA': []}
        ppb = PDB.PPBuilder()
        for pp in ppb.build_peptides(self.structure):
            sequences['Protein'].append(str(pp.get_sequence()))
        for model in self.structure:
            for chain in model:
                dna_sequence, rna_sequence = [], []
                for residue in chain:
                    if residue.resname in ["DA", "DT", "DC", "DG"]:
                        dna_sequence.append(residue.resname)
                    elif residue.resname in ["A", "U", "C", "G"]:
                        rna_sequence.append(residue.resname)
                if dna_sequence:
                    sequences['DNA'].append(''.join(dna_sequence))
                if rna_sequence:
                    sequences['RNA'].append(''.join(rna_sequence))
        return sequences
    
    def c_alpha_coords(self):
      c_alpha_coords = {}
      for model in self.structure:
          for chain in model:
              chain_coords = []
              for residue in chain:
                  if "CA" in residue:
                      ca_atom = residue["CA"]
                      chain_coords.append(ca_atom.coord.tolist())  # Convert ndarray to list
              if chain_coords:
                  c_alpha_coords[chain.id] = chain_coords
      return c_alpha_coords if c_alpha_coords else "Cα coordinates not found"

    def refinement_resolution(self):
        resolution = self.structure.header.get("resolution", "Resolution information not found")
        if resolution == "Resolution information not found":
            for line in self.pdb_lines:
                if line.startswith("REMARK   2 RESOLUTION."):
                    resolution = line.split()[-2]
                    break
        return resolution

    def experiment_type(self):
        exp_type = self.structure.header.get("structure_method", "Structure method information not found")
        if exp_type == "Structure method information not found":
            for line in self.pdb_lines:
                if line.startswith("EXPDTA"):
                    exp_type = " ".join(line.split()[1:])
                    break
        return exp_type

    def enzyme_classification(self):
        ec = self.structure.header.get("compound", {}).get("ec", "Enzyme Classification not found")
        if ec == "Enzyme Classification not found":
            ec = "N/A"
        return ec

    def symmetry_type(self):
        sym_type = self.structure.header.get("symmetry", "Symmetry Type not found")
        if sym_type == "Symmetry Type not found":
            for line in self.pdb_lines:
                if line.startswith("CRYST1"):
                    sym_type = line[55:].strip()
                    break
        return sym_type

    def r_factor(self):
        for line in self.pdb_lines:
            if "REMARK   3   R VALUE" in line:
                r_factor = line.split()[-1]
                return r_factor
        return "N/A"

    def b_factor(self):
        b_factors = []
        for model in self.structure:
            for chain in model:
                for residue in chain:
                    if 'CA' in residue:
                        b_factors.append(residue['CA'].get_bfactor())
        return sum(b_factors) / len(b_factors) if b_factors else "N/A"

"""
#EXAMPLE USAGE IN COLAB WAS THIS
# Example usage
folder_path = '/content/drive/MyDrive/expl'
processor = PDBProcessor(folder_path)

"""