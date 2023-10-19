import csv
import os
import multiprocessing
from Functions2 import PDBProcessor

def process_file(file_path):
    pdb_processor = PDBProcessor(file_path)
    results = pdb_processor.process()
    file_code = os.path.basename(file_path).split('.')[0].upper()
    return file_code, results

def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    pdb_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.pdb')]

    if not pdb_files:
        print(f"No .pdb files found in {folder_path}.")
        return

    results_dict = {}
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_file, pdb_files)
        for code, result in results:
            results_dict[code] = result
            print(f"Processed: {code}")

    return results_dict

def save_results_to_csv(data_dict, csv_filename):
    if not data_dict:
        print("No data to save to CSV.")
        return

    rows = []
    for protein_name, details in data_dict.items():
        row = {"protein_name": protein_name, **details}
        rows.append(row)

    fieldnames = ["protein_name", "Polymer_Entity", "Refinement_Resolution",
                  "Experiment_Type", "Sequence", "Enzyme_Classification",
                  "Symmetry_Type", "C_alpha_Coords"]

    try:
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(rows)
        print(f"Saved data to {csv_filename}.")
    except IOError as e:
        print(f"Error saving data to {csv_filename}: {e}")

if __name__ == "__main__":
    folder_path = "/content/drive/MyDrive/SimplePDBFiles"
    results_dict = process_folder(folder_path)
    save_results_to_csv(results_dict, "output.csv")
