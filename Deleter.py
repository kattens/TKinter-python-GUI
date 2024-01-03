import os

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
                try:
                    with open(pdb_file_path, 'r') as pdb_file:
                        lines = pdb_file.readlines()
                        if any(self.keyword in line for line in lines[:100]):
                            try:
                                os.remove(pdb_file_path)
                                self.num_deleted_files += 1
                                self.deleted_file_names.append(filename)
                                print(f"Deleted {filename}")
                            except PermissionError as e:
                                print(f"Permission error while deleting {filename}: {e}")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

        print(f"Total {self.keyword} files removed: {self.num_deleted_files}")
        if self.num_deleted_files > 0:
            print("Deleted files:", ', '.join(self.deleted_file_names))

class DNADelete(FileDeleter):
    def __init__(self, directory_path):
        super().__init__(directory_path, "DNA")

class NMRDelete(FileDeleter):
    def __init__(self, directory_path):
        super().__init__(directory_path, "NMR")
