"""
we have to add functions for deleting files here before doing the sequence building:

Functions to be defined = columns
- r factor/ value
- b factor/ value
- sequence of the protein/rna/dna
- c-alpha coords
- is it dna/rna/protein/or hybrid= polymer entity
- taxonomy
- resolution number = refinement resolution
- experiment type
- enzyme classification
- symmetry type
"""

import os
import time

class FileDeleter:
    def __init__(self, directory_path, keyword):
        self.directory_path = directory_path
        self.keyword = keyword
        self.num_deleted_files = 0
        self.deleted_file_names = []

    def delete_files(self):
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".pdb"):
                pdb_file_path = os.path.join(self.directory_path, filename)
                with open(pdb_file_path, 'r') as pdb_file:
                    lines = pdb_file.readlines()
                    
                    if any(self.keyword in line for line in lines[:100]):
                        pdb_file.close()  # Explicitly close the file
                        
                        # Attempt to delete the file with multiple retries
                        for _ in range(3):  
                            try:
                                time.sleep(0.5)  # A half-second delay
                                os.remove(pdb_file_path)
                                break  # Break out of the loop if the deletion was successful
                            except PermissionError:
                                time.sleep(0.5)  # Wait for half a second before trying again

                self.num_deleted_files += 1
                self.deleted_file_names.append(filename)

        print(f"Total {self.keyword} files removed: {self.num_deleted_files}")
        print(f"Deleted files: {self.deleted_file_names}")

class DNADelete(FileDeleter):
    def __init__(self, directory_path):
        super().__init__(directory_path, "DNA")

class NMRDelete(FileDeleter):
    def __init__(self, directory_path):
        super().__init__(directory_path, "NMR")


