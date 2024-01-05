import tkinter as tk
from tkinter import filedialog, messagebox

# Assuming that PDBDownloader, PDBChainSplitter, DNADelete, NMRDelete, and PDBProcessor are correctly implemented and imported
from PDB_Downloader import PDBDownloader
from Chain_Seperator import PDBChainSplitter
from Deleter import DNADelete, NMRDelete
from PDBProcessor import PDBProcessor

# Global variables
global_output_path = ""
global_csv_file_path = ""  # Added global variable for CSV file path

# --- Functions ---
def browse_file():
    """Function to browse and select a CSV file."""
    global global_csv_file_path  # Access the global variable
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, csv_file_path)
        global_csv_file_path = csv_file_path  # Update the global variable



def browse_output_directory():
    """Function to browse and select an output directory and update global_output_path."""
    global global_output_path  # Access the global variable

    output_directory = filedialog.askdirectory()
    if output_directory:
        entry_output_directory.delete(0, tk.END)
        entry_output_directory.insert(0, output_directory)
        global_output_path = output_directory  # Update the global variable


def split_pdb_chains():
    """Function to split PDB chains."""
    if not global_output_path:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    try:
        pdb_splitter = PDBChainSplitter(global_output_path, global_output_path)
        pdb_splitter.process_pdb_files()
        messagebox.showinfo("Process Complete", "Separation of PDB files is complete!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def export_selected_elements():
    """Function to process selected PDB file elements."""
    if not global_output_path:
        messagebox.showerror("Error", "Output path not set.")
        return

    selected_methods = [element for element, var in zip(elements, vars_elements) if var.get()]

    if not selected_methods:
        messagebox.showinfo("No Selection", "Please select at least one method.")
        return

    # Assuming you have a function in PDBProcessor to process and save the data
    processor = PDBProcessor(global_output_path, selected_methods)
    processor.process_all_pdb_files()  # Process the files using the selected methods

    messagebox.showinfo("Process Complete", "Processing of PDB files is complete!")

def download_pdb():
    """ Function to download pdb files"""
    if not global_output_path:
        messagebox.showerror("Error", "Output path not set.")
        return
    
    downloader = PDBDownloader(global_output_path, global_csv_file_path)
    downloader.download_pdb()
    messagebox.showinfo("Process Complete", "Downloading of PDB files is complete!")


# --- Main Application ---
app = tk.Tk()
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
tk.Button(frame_buttons, text="Export Elements", command=export_selected_elements).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Split PDB Chains", command=split_pdb_chains).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Download PDB", command=download_pdb).pack(side=tk.LEFT, padx=5)


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
