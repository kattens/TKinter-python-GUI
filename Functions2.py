import os
import multiprocessing
from Bio.PDB import PDBParser, Polypeptide
from Bio.PDB.Polypeptide import is_aa, three_to_one

class PDBProcessor:
    def __init__(self, file_path, methods_to_call=None):
        self.file_path = file_path
        self.parser = PDBParser(QUIET=True)
        self.structure = self.parser.get_structure("structure", self.file_path)
        if methods_to_call is None:
            self.methods_to_call = [
                "Polymer_Entity",
                "Refinement_Resolution",
                "Experiment_Type",
                "Sequence",
                "Enzyme_Classification",
                "Symmetry_Type",
                "C_alpha_Coords",
            ]
        else:
            self.methods_to_call = methods_to_call

    def process(self):
        results = {}
        for method_name in self.methods_to_call:
            method = getattr(self, method_name, None)
            if callable(method):
                results[method_name] = method()
        return results

    def Polymer_Entity(self):
        criteria = {"DNA": False, "Protein": False, "RNA": False}

        for model in self.structure:
            for chain in model:
                for residue in chain:
                    if residue.resname in ["DA", "DT", "DC", "DG"]:
                        criteria["DNA"] = True
                    elif residue.resname in ["A", "U", "C", "G"]:
                        criteria["RNA"] = True
                    else:
                        criteria["Protein"] = True

        if criteria["DNA"] and not criteria["Protein"] and not criteria["RNA"]:
            return "DNA"
        elif criteria["Protein"] and not criteria["DNA"] and not criteria["RNA"]:
            return "Protein"
        elif criteria["RNA"] and not criteria["DNA"] and not criteria["Protein"]:
            return "RNA"
        else:
            return "Hybrid"

    def Refinement_Resolution(self):
        return self.structure.header.get("resolution", "Resolution information not found")

    def Experiment_Type(self):
        return self.structure.header.get("structure_method", "Structure method information not found")

    def Sequence(self):
        sequences = {}
        for model in self.structure:
            for chain in model:
                protein_sequence = []
                dna_sequence = []
                rna_sequence = []
                for residue in chain:
                    if is_aa(residue):  # Amino acids for proteins
                        try:
                            protein_sequence.append(three_to_one(residue.resname))
                        except KeyError:
                            if residue.resname == 'MSE':
                                protein_sequence.append('M')  # Treat MSE as Methionine
                            else:
                                continue  # Skip any other non-standard amino acids
                    else:
                        if residue.resname in ["DA", "DT", "DC", "DG"]:  # DNA nucleotides
                            dna_sequence.append(residue.resname)
                        elif residue.resname in ["A", "U", "C", "G"]:  # RNA nucleotides
                            rna_sequence.append(residue.resname)

                if protein_sequence:
                    sequences[f'{chain.id}_protein'] = ''.join(protein_sequence)

                # Check the type of nucleotide sequence
                if dna_sequence and not rna_sequence:
                    sequences[f'{chain.id}_DNA'] = ''.join(dna_sequence)
                elif rna_sequence and not dna_sequence:
                    sequences[f'{chain.id}_RNA'] = ''.join(rna_sequence)
                elif dna_sequence and rna_sequence:
                    # If both DNA and RNA are present in the same chain, it's a hybrid
                    sequences[f'{chain.id}_DNA_RNA_hybrid'] = ''.join(dna_sequence + rna_sequence)
        return sequences

    def Enzyme_Classification(self):
        return self.structure.header.get("compound", {}).get("ec", "Enzyme Classification not found")

    def Symmetry_Type(self):
        return self.structure.header.get("symmetry", "Symmetry Type not found")

    def C_alpha_Coords(self):
        c_alpha_coords = {}
        for model in self.structure:  # Change 'this.structure' to 'self.structure'
            for chain in model:
                chain_coords = []
                for residue in chain:
                    if "CA" in residue:  # Check if Cα atom is present in the residue
                        ca_atom = residue["CA"]
                        chain_coords.append(ca_atom.coord)  # Appending the (x,y,z) tuple of the Cα atom
                if chain_coords:
                    c_alpha_coords[chain.id] = chain_coords
        return c_alpha_coords if c_alpha_coords else "Cα coordinates not found"




