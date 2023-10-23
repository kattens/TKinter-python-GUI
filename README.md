# Usage Instructions:
1. Download all the files as a complete package, then execute the GUI code file. The application will open, enabling you to download and manage files, creating your preferred dataset for various purposes.

# Upcoming Additions to this Repository:
1. A readily available dataset for users who simply want something to work with.
2. A Python package for those who wish to modify the core code to meet their specific requirements, eliminating the need to start from scratch.

# Data Cleaning Procedure:

We are working with a dataset containing protein names from the PDB site, and our goal is to streamline the data-cleaning process using automated methods. While manual downloading is possible on the site, we aim to create a code that can handle this task efficiently.

Here's the step-by-step process we'll follow:

1. **Data Retrieval and Initial Filtering:**
   We will initiate the process by extracting protein names from the PDB site. Our code will then automatically download the corresponding files. This approach simplifies data scraping and enhances efficiency, providing a structured dataset. While direct manual downloads are feasible, automation offers more streamlined handling.

2. **Categorization of Protein Types:**
   After the initial download, we will categorize the proteins based on their types. Proteins that are DNAs (NMR) and EM (complexes) will be identified and segregated into a separate CSV file. This segregation ensures that the dataset remains organized and suitable for downstream analyses.

3. **Refining the Dataset:**
   We will proceed by eliminating undesired data points. This involves removing proteins with low resolutions and excluding those that are not based on X-ray experiment types. This refinement step ensures that the dataset consists of high-quality, relevant protein structures for further processing.

4. **Handling Multi-Chain Files:**
   For proteins composed of multiple chains, such as the example 1abc with 2 chains, we will create distinct entries for each chain. This separation results in entries like 1abc_1 and 1abc_2. By doing this, we maintain granularity in our dataset, enabling more precise analyses.

5. **3D Coordinate List Creation:**
   We will compile a comprehensive list of 3D coordinates from the protein structures. These coordinates will be retained in their original form, without tokenization, to serve as informative labels. This step facilitates the preservation of structural information for downstream tasks.

6. **Sequence Tokenization:**
   To process protein sequences, we will utilize a tokenizer. In Phase 1, we used a BERT tokenizer; however, we have recognized the potential of the Protrans tokenizer to be more suitable for our needs. Tokenizing sequences allows us to convert them into a format compatible with machine learning models.

7. **Note on Tokenization Outcome:**
   It's essential to note that the tokenizer's output will consist of IDs representing the tokenized sequences, rather than full vectors. This design decision is influenced by the underlying architecture of the model and facilitates access to information in deeper layers for subsequent analyses.

By following this refined data cleaning procedure, we aim to establish a well-structured and comprehensive dataset that can be effectively utilized for various analyses and modeling tasks.
