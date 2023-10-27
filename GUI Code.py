import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os
from PDB_Downloader import PDBDownloader
from Chain_Seperator import PDBChainSplitter
from Deleter import DNADelete, NMRDelete
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

# Create Frames
pdb_frame = ttk.LabelFrame(root, text="PDB File Management")
csv_frame = ttk.LabelFrame(root, text="CSV Management")

# Grid layout for frames
pdb_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
csv_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# PDB File Management Frame
tk.Label(pdb_frame, text="Select an output directory:").pack(pady=5)
entry_output_directory = tk.Entry(pdb_frame)
entry_output_directory.pack(pady=5)
tk.Button(pdb_frame, text="Browse Output", command=browse_output_directory).pack(pady=5)
tk.Button(pdb_frame, text="Process", command=process_file).pack(pady=5)
tk.Button(pdb_frame, text="Separate Chains", command=split_pdb_chains).pack(pady=5)
tk.Button(pdb_frame, text="Remove NMR", command=remove_nmr).pack(pady=5)
tk.Button(pdb_frame, text="Remove DNA", command=remove_dna).pack(pady=5)

# CSV Management Frame
tk.Label(csv_frame, text="Select a CSV file:").pack(pady=5)
entry_file_path = tk.Entry(csv_frame)
entry_file_path.pack(pady=5)
tk.Button(csv_frame, text="Browse CSV", command=browse_file).pack(pady=5)
tk.Button(csv_frame, text="Create Empty CSV and Process Functions", command=create_empty_csv_and_process).pack(pady=5)

# Element Selection Section
tk.Label(csv_frame, text="Please choose your elements:").pack(pady=5)
element_frame = tk.Frame(csv_frame)
element_frame.pack(padx=20, pady=10)
elements = ["Protein_Name", "Polymer_Entity", "Sequence", "C-alpha_Coords", "Refinement_Resolution", "Experiment_Type", "Enzyme_Classification", "Taxonomy", "B_Factor", "R_Factor", "Symmetry_Type"]
var = [tk.IntVar() for _ in elements]
for idx, element in enumerate(elements):
    ttk.Checkbutton(element_frame, text=element, variable=var[idx]).pack(anchor="w")

# Configure column weights for resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start main loop
root.mainloop()
