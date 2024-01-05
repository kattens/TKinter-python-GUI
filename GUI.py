import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox

from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Import your existing processing classes
from PDB_Downloader import PDBDownloader
from Chain_Seperator import PDBChainSplitter
from PDBProcessor import PDBProcessor

class VideoSplashScreen(QWidget):
    def __init__(self, video_path, parent=None):
        
        super().__init__(parent)
        self.setMinimumSize(1800, 1200)
        self.setWindowTitle("Splash Screen")
        self.setGeometry(600, 300, 600, 400)
        self.player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)
        self.player.setVideoOutput(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.player.play()
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.close()


class PDBManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 640, 480)

        self.global_output_path = ""
        self.global_csv_file_path = ""

        self.initUI()

    def initUI(self):
        # Create layout
        layout = QVBoxLayout()

        # File path section
        file_path_layout = QHBoxLayout()
        self.entry_file_path = QLineEdit()
        file_path_layout.addWidget(QLabel("CSV File Path:"))
        file_path_layout.addWidget(self.entry_file_path)
        file_path_btn = QPushButton("Browse")
        file_path_btn.clicked.connect(self.browse_file)
        file_path_layout.addWidget(file_path_btn)

        # Output directory section
        output_dir_layout = QHBoxLayout()
        self.entry_output_directory = QLineEdit()
        output_dir_layout.addWidget(QLabel("Output Directory:"))
        output_dir_layout.addWidget(self.entry_output_directory)
        output_dir_btn = QPushButton("Browse")
        output_dir_btn.clicked.connect(self.browse_output_directory)
        output_dir_layout.addWidget(output_dir_btn)

        # Buttons section
        buttons_layout = QHBoxLayout()
        export_btn = QPushButton("Export Elements")
        export_btn.clicked.connect(self.export_selected_elements)
        split_btn = QPushButton("Split PDB Chains")
        split_btn.clicked.connect(self.split_pdb_chains)
        download_btn = QPushButton("Download PDB")
        download_btn.clicked.connect(self.download_pdb)
        buttons_layout.addWidget(export_btn)
        buttons_layout.addWidget(split_btn)
        buttons_layout.addWidget(download_btn)

        # Checkboxes for elements
        self.elements = [
            "protein_name", "polymer_entity", "refinement_resolution",
            "experiment_type", "sequence", "enzyme_classification",
            "symmetry_type", "c_alpha_coords", 'r_factor'
        ]
        elements_layout = QHBoxLayout()
        self.vars_elements = []
        for element in self.elements:
            cb = QCheckBox(element)
            elements_layout.addWidget(cb)
            self.vars_elements.append(cb)

        # Add layouts to main layout
        layout.addLayout(file_path_layout)
        layout.addLayout(output_dir_layout)
        layout.addLayout(buttons_layout)
        layout.addLayout(elements_layout)

        # Set main layout
        self.setLayout(layout)
        self.setWindowTitle("BioPDBKit")
        self.setGeometry(600, 600, 800, 350)

    def browse_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "CSV Files (*.csv)", options=options)
        if fileName:
            self.entry_file_path.setText(fileName)
            self.global_csv_file_path = fileName

    def browse_output_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if directory:
            self.entry_output_directory.setText(directory)
            self.global_output_path = directory

    def split_pdb_chains(self):
        """Function to split PDB chains."""
        if not self.global_output_path:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return

        try:
            pdb_splitter = PDBChainSplitter(self.global_output_path, self.global_output_path)
            pdb_splitter.process_pdb_files()
            QMessageBox.information(self, "Process Complete", "Separation of PDB files is complete!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def export_selected_elements(self):
        """Function to process and export selected elements."""
        if not self.global_output_path:
            QMessageBox.warning(self, "Error", "Output path not set.")
            return

        # Assuming you have a function in PDBProcessor to process and save the data
        processor = PDBProcessor(self.global_output_path)
        processor.process_all_pdb_files()  # Process the files using the selected methods

        QMessageBox.information(self, "Process Complete", "Processing of PDB files is complete!")

    def download_pdb(self):
        """Function to download PDB files."""
        if not self.global_output_path or not self.global_csv_file_path:
            QMessageBox.warning(self, "Error", "Please set both output path and CSV file path.")
            return

        try:
            downloader = PDBDownloader(self.global_output_path, self.global_csv_file_path)
            downloader.download_pdb()
            QMessageBox.information(self, "Process Complete", "Downloading of PDB files is complete!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_video = "C:\\Users\\KATT\\Documents\\BioPDBKit\\intro.mp4"
    splash = VideoSplashScreen(splash_video)
    splash.show()

    ex = PDBManagerApp()
    ex.show()

    sys.exit(app.exec_())