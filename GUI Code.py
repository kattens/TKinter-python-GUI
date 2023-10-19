import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os
from PDB_Downloader import PDBDownloader
from Chain_Seperator import PDBChainSplitter
from Functions import DNADelete, NMRDelete
from Functions2 import PDBProcessor
#from csvAdder import process_folder,save_results_to_csv

# --- Functions ---
def browse_file():
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, csv_file_path)

def browse_output_directory():
    output_directory = filedialog.askdirectory()
    entry_output_directory.delete(0, tk.END)
    entry_output_directory.insert(0, output_directory)

def process_file():
    csv_file_path = entry_file_path.get()
    output_directory = entry_output_directory.get()

    if not csv_file_path or not output_directory:
        messagebox.showerror("Error", "Please select a CSV file and output directory.")
        return

    with open(csv_file_path, 'r') as csv_in:
        protein_names = [row[0] for row in csv.reader(csv_in)][1:]

    downloader = PDBDownloader(output_directory)
    downloader.download_pdb(protein_names)

    messagebox.showinfo("Process Complete", "Downloading of PDB files is complete!")

def split_pdb_chains():
    input_folder = entry_output_directory.get()
    pdb_splitter = PDBChainSplitter(input_folder, input_folder)
    pdb_splitter.process_pdb_files()
    messagebox.showinfo("Process Complete", "Separating of PDB files is complete!")

def remove_nmr():
    nmr_deleter = NMRDelete(entry_output_directory.get())
    nmr_deleter.delete_files()
    messagebox.showinfo("Process Complete", "NMR-related PDB files have been removed!")

def remove_dna():
    dna_deleter = DNADelete(entry_output_directory.get())
    dna_deleter.delete_files()
    messagebox.showinfo("Process Complete", "DNA-related PDB files have been removed!")

#DOnt forget to use the full_file_path as the initial value for the Functions
#since it would be easier to create and do the functions at the same time we will go with this approach
def create_empty_csv_and_process():
    column_names_modified = ["Protein_Name", "Polymer_Entity", "Sequence", "C-alpha_Coords", "Refinement_Resolution", "Experiment_Type", "Enzyme_Classification", "Taxonomy", "B_Factor", "R_Factor", "Symmetry_Type"]
    output_path = filedialog.askdirectory(title="Please set your output path:")
    csv_file_name = filedialog.asksaveasfilename(defaultextension=".csv", title="Please set your csv file name:")
    full_file_path = os.path.join(output_path, csv_file_name)
    with open(full_file_path, 'w', newline='') as csv_file:
        csv.writer(csv_file).writerow(column_names_modified)
    messagebox.showinfo("Info", f"Empty CSV file with column names created at '{full_file_path}'")
    """
    # Process the folder and save results to the CSV file
    processor = PDBProcessor(full_file_path)  # Adjust this as needed
    folder_path = "/content/drive/MyDrive/SimplePDBFiles"  # Set your folder path here
    results_dict = process_folder(folder_path)
    save_results_to_csv(results_dict, full_file_path)
"""
    # Create a messagebox here for adding the details to columns
    return full_file_path  
 

# --- Main App ---
root = tk.Tk()
root.title("PDB File Downloader")
root.geometry("800x500")

# UI for CSV and Directory selection
tk.Label(root, text="Select a CSV file:").pack()
entry_file_path = tk.Entry(root)
entry_file_path.pack()
tk.Button(root, text="Browse CSV", command=browse_file).pack()

tk.Label(root, text="Select an output directory:").pack()
entry_output_directory = tk.Entry(root)
entry_output_directory.pack()
tk.Button(root, text="Browse Output", command=browse_output_directory).pack()

# Buttons for processing
tk.Button(root, text="Process", command=process_file).pack()
tk.Button(root, text="Separate Chains", command=split_pdb_chains).pack()
tk.Button(root, text="Remove NMR", command=remove_nmr).pack()
tk.Button(root, text="Remove DNA", command=remove_dna).pack()

# Element Selection Section
tk.Label(root, text="Please choose your elements:").pack()
element_frame = tk.Frame(root)
element_frame.pack(padx=20, pady=10)
elements = ["Protein_Name", "Polymer_Entity", "Sequence", "C-alpha_Coords", "Refinement_Resolution", "Experiment_Type", "Enzyme_Classification", "Taxonomy", "B_Factor", "R_Factor", "Symmetry_Type"]
var = [tk.IntVar() for _ in elements]
for idx, element in enumerate(elements):
    ttk.Checkbutton(element_frame, text=element, variable=var[idx]).pack(anchor="w")

# Create an empty CSV button
tk.Button(root, text="Create Empty CSV and Process Functions", command=create_empty_csv_and_process).pack()

root.mainloop()
