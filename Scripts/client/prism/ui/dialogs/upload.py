from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


# Create an "Uploading" dialog for the user to see while the file is being uploaded
class UploadDialog(QDialog):
    def __init__(self):
        super(UploadDialog, self).__init__()
        self.setWindowTitle("Slack Upload")
        self.setModal(True)
        self.setLayout(QVBoxLayout())

        self.label = QLabel("Uploading to Slack...")
        self.layout().addWidget(self.label)
