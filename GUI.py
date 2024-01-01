import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os

# Assuming that PDBDownloader, PDBChainSplitter, DNADelete, NMRDelete, and PDBProcessor are correctly implemented and imported
from PDB_Downloader import PDBDownloader
from Chain_Seperator import PDBChainSplitter
from Deleter import DNADelete, NMRDelete
from PDBProcessor import PDBProcessor

# Global variable to store the output directory
global_output_path = None

# --- Functions ---
def browse_file():
    """Function to browse and select a CSV file."""
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, csv_file_path)

def browse_output_directory():
    """Function to browse and select an output directory."""
    output_directory = filedialog.askdirectory()
    if output_directory:
        entry_output_directory.delete(0, tk.END)
        entry_output_directory.insert(0, output_directory)









"""FILES THAT ARE CHECKED TO BE CORRECT"""
        
def process_file(output_directory, protein_names):
    """Function to process selected CSV file/list and download PDB files."""
    try:
        downloader = PDBDownloader(output_directory, protein_names)
        downloader.download_pdb()  # Assuming this method downloads the files

        messagebox.showinfo("Process Complete", "Downloading of PDB files is complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def split_pdb_chains():
    """Function to split PDB chains."""
    input_folder = entry_output_directory.get()
    if not input_folder:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    try:
        pdb_splitter = PDBChainSplitter(input_folder, input_folder)
        pdb_splitter.process_pdb_files()
        messagebox.showinfo("Process Complete", "Separating of PDB files is complete!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

























#for setting the global output
def browse_output_directory():
    """Function to browse and select an output directory and update global_output_path."""
    global global_output_path  # Access the global_output_path variable

    output_directory = filedialog.askdirectory()
    if output_directory:
        entry_output_directory.delete(0, tk.END)
        entry_output_directory.insert(0, output_directory)
        
        # Update the global_output_path
        global_output_path = output_directory  # Set the global_output_path to the selected directory








#FIGURE SOMETHING OUT FO THE DELETER
def remove_nmr():
    """Function to remove NMR-related PDB files."""
    try:
        nmr_deleter = NMRDelete(entry_output_directory.get())
        nmr_deleter.delete_files()
        messagebox.showinfo("Process Complete", "NMR-related PDB files have been removed!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def remove_dna():
    """Function to remove DNA-related PDB files."""
    try:
        dna_deleter = DNADelete(entry_output_directory.get())
        dna_deleter.delete_files()
        messagebox.showinfo("Process Complete", "DNA-related PDB files have been removed!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")











# Global variables to store GUI elements
elements = ["Polymer_Entity", "Refinement_Resolution", "Experiment_Type", "Sequence", 
            "Enzyme_Classification", "Symmetry_Type", "C_alpha_Coords"]
vars_elements = []  # Store tkinter BooleanVar instances for each checkbox element
def export_selected_elements():
    """Function to export selected elements."""
    global global_output_path  # Use the global output path

    # Check which elements are selected by the user
    selected_elements = [element for element, var in zip(elements, vars_elements) if var.get()]

    if not selected_elements:
        messagebox.showinfo("No Selection", "Please select at least one element.")
        return

    if not global_output_path:
        messagebox.showerror("Error", "Output path not set.")
        return

    # Create the file path for exporting
    #file_path = os.path.join(global_output_path, "selected_elements.csv")
    file_path = global_output_path
    # Process the PDB file using the selected elements
    processor = PDBProcessor(file_path, selected_elements)
    results = processor.process()

    # Create a summary of the results to display
    summary = []
    for element in selected_elements:
        summary.append(f"{element}: {results.get(element, 'Data not found')}")

    # Show the summary in a messagebox
    summary_text = '\n'.join(summary)
    messagebox.showinfo("Results", summary_text)







# --- Main Application ---
app = app = tk.Tk()
app.title("PDB Management Tool")

frame_file = tk.Frame(app)
frame_file.pack(pady=5)
tk.Label(frame_file, text="CSV File Path:").pack(side=tk.LEFT, padx=5)
entry_file_path = tk.Entry(frame_file, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)
tk.Button(frame_file, text="Browse", command=browse_file).pack(side=tk.LEFT, padx=5)

frame_output_directory = tk.Frame(app)
frame_output_directory.pack(pady=5)
tk.Label(frame_output_directory, text="Output Directory:").pack(side=tk.LEFT, padx=5)
entry_output_directory = tk.Entry(frame_output_directory, width=50)
entry_output_directory.pack(side=tk.LEFT, padx=5)
tk.Button(frame_output_directory, text="Browse", command=browse_output_directory).pack(side=tk.LEFT, padx=5)

frame_buttons = tk.Frame(app)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="Download PDB", command=process_file).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Split PDB Chains", command=split_pdb_chains).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Remove NMR Files", command=remove_nmr).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Remove DNA Files", command=remove_dna).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Export Selected Elements", command=export_selected_elements).pack(side=tk.LEFT, padx=5)




frame_elements = tk.Frame(app)
frame_elements.pack(pady=10)


elements = [
    "Polymer_Entity",
    "Refinement_Resolution",
    "Experiment_Type",
    "Sequence",
    "Enzyme_Classification",
    "Symmetry_Type",
    "C_alpha_Coords",
]
vars_elements = []
for element in elements:
    var = tk.IntVar()
    tk.Checkbutton(frame_elements, text=element, variable=var).pack(side=tk.LEFT, padx=5)
    vars_elements.append(var)

app.mainloop()