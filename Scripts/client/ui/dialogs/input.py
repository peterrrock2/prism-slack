import os
from pathlib import Path

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


# Create dialog used to input things like the Slack OAuth token or the App-Level Token
class InputDialog(QDialog):
    def __init__(self, title):
        super(InputDialog, self).__init__()

        self.setWindowTitle("Slack")
        self.setModal(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(title)
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.button_layout = QHBoxLayout()
        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")
        self.button_layout.addWidget(self.button_ok)
        self.button_layout.addWidget(self.button_cancel)

        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.layout.addLayout(self.button_layout)

    def get_input(self):
        return self.input_field.text()
