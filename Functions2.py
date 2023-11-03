
from Bio import PDB
from Bio.PDB.Polypeptide import is_aa

class PDBProcessor:
    def __init__(self, file_path):
        self.structure = PDB.PDBParser(QUIET=True).get_structure('PDB', file_path)
        with open(file_path, 'r') as f:
            self.pdb_lines = f.readlines()

    def protein_name(self):
        for model in self.structure:
            for chain in model:
                for residue in chain:
                    if is_aa(residue):
                        return residue.id[0]
        return "N/A"

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
        sequences = {}
        ppb = PDB.PPBuilder()
        for pp in ppb.build_peptides(self.structure):
            sequences['Protein'] = str(pp.get_sequence())
        for model in self.structure:
            for chain in model:
                dna_sequence = []
                rna_sequence = []
                for residue in chain:
                    if residue.resname in ["DA", "DT", "DC", "DG"]:
                        dna_sequence.append(residue.resname)
                    elif residue.resname in ["A", "U", "C", "G"]:
                        rna_sequence.append(residue.resname)
                if dna_sequence:
                    sequences[f'{chain.id}_DNA'] = ''.join(dna_sequence)
                if rna_sequence:
                    sequences[f'{chain.id}_RNA'] = ''.join(rna_sequence)
        return sequences

    def c_alpha_coords(self):
        c_alpha_coords = {}
        for model in self.structure:
            for chain in model:
                chain_coords = []
                for residue in chain:
                    if "CA" in residue:
                        ca_atom = residue["CA"]
                        chain_coords.append(ca_atom.coord)
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
            # PDB files typically don't contain enzyme classification. You'd need to access an external database for this.
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

