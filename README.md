# BioPDBKit: The ultimate PDB Dataset Toolkit

## Overview
The Ultimate PDB Dataset Toolkit is a resource aimed to ease the process of accessing and using protein data. This toolkit is perfect for individuals in bioinformatics, machine learning, and NLP, whether they're beginners or seasoned professionals.

If you're new to the world of biology and PDB files, don't worry – we've got you covered. We've curated a documentation that provides a high-level description essential for getting started. We aimed to create a resource that's both compact and comprehensive, offering just enough detail to understand the essentials without overwhelming you. 
The document: (Detailed_Exploration_of_Biological_Molecules_and_PDB_Files)

## Features
- **Ultimate PDB Dataset**: A robust dataset originating from authentic biological experiments, encompassing data on about 75,000 organisms. This expands to nearly 200,000 unique biological profiles when considering individual chains of proteins, DNA, or RNA.
- **Customizable Data Selection**: A set of tools that enable you to handpick and modify datasets to fit the exact needs of your project. These tools support both JSON and CSV formats and include a user-friendly GUI for ease of use.
CSV link:https://www.kaggle.com/datasets/kattens/biopdbkit
Json link: (to be announced)
 
- **BioPDBKit**: A specialized Python package for those who prefer a more hands-on approach to data manipulation, suitable for advanced users.

## Getting Started

### Installation
Install the toolkit via pip with this simple command:
```
pip install BioPDBKit
```

### Downloading PDB Files
1. Identify and list the PDB files you require.
2. Input these names into our downloader, either directly or via a CSV file with the names in the first column.
3. The downloader will efficiently gather these files into a designated directory for your convenience.

### Dataset Customization
- Our GUI provides an intuitive platform for dataset customization, allowing you to select only the data relevant to your project.
- For those preferring ready-made solutions, we offer pre-compiled datasets in JSON and CSV formats, tailored to common use cases.

### Using BioPDBKit
- BioPDBKit is ideal for users with programming expertise who wish to engage deeply with data manipulation.
- The package allows intricate operations on protein data, enhancing the possibilities for your research and development.
- Detailed documentation is provided for guidance and best practices.

## Dataset Composition
**Included Fields**:
- Protein name, experiment type, protein sequence, resolution, R factor-value, chain ID, secondary structure, and b-factor/value.

**Excluded Fields** (for clarity and focus):
- PDB ID, release date, authors, organism details, and atom numbers for various components.

## Objective
Our toolkit's primary goal is to simplify the process of creating datasets for machine learning and NLP applications. It is particularly suited for tasks such as classification, structure prediction, and protein-protein interaction (PPI) classification.

## Example Application
We have utilized this toolkit to develop a Bert-based model for classification tasks. This model is a testament to the dataset's quality, with unique tweaks in its hidden layers showcasing the dataset's versatility. Comprehensive details about our methods and findings will be shared in the near future.

## Contributing
We welcome contributions to enhance the Ultimate PDB Dataset Toolkit. Please refer to our contribution guidelines for more information on how to submit your proposals or improvements.


- Recognition of any supporting institutions, grants, or collaborative efforts.
