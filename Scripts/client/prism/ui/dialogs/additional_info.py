from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


# Create Dialog for the user to input comments for the Slack Post
class AdditionalInfoDialog(QDialog):
    def __init__(self):
        super(AdditionalInfoDialog, self).__init__()

        plugin_directory = Path(__file__).resolve().parents[2]

        self.setWindowTitle("Slack Publish Information")
        self.setWindowIcon(
            QIcon(os.path.join(plugin_directory, "Resources", "slack-icon.png"))
        )
        self.setModal(True)
        self.setLayout(QVBoxLayout())
        self.buttonLayout = QHBoxLayout()

        self.label = QLabel("Please leave your additional comments below (optional)")
        self.layout().addWidget(self.label)

        self.text_edit = QTextEdit()
        self.layout().addWidget(self.text_edit)

        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")

        self.div = QFrame()
        self.div.setFrameShape(QFrame.HLine)
        self.div.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.div)

        self.gb_status = QGroupBox("Status")
        self.bg_status = QButtonGroup()
        self.lo_review = QHBoxLayout()
        self.gb_status.setLayout(self.lo_review)

        self.rb_status_wip = QRadioButton("Work In Progress")
        self.rb_status_wip.setStyleSheet(
            """QRadioButton::indicator { width: 15px; height: 15px; }"""
        )
        self.rb_status_wip.setChecked(True)
        self.lo_review.addWidget(self.rb_status_wip)

        self.rb_status_reivew = QRadioButton("Request Review")
        self.rb_status_reivew.setStyleSheet(
            """QRadioButton::indicator { width: 15px; height: 15px; }"""
        )
        self.lo_review.addWidget(self.rb_status_reivew)

        self.bg_status.addButton(self.rb_status_wip)
        self.bg_status.addButton(self.rb_status_reivew)
        self.layout().addWidget(self.gb_status)

        self.buttonLayout.addWidget(self.button_ok)
        self.buttonLayout.addWidget(self.button_cancel)
        self.layout().addLayout(self.buttonLayout)

        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

    # Get the comments from the text edit box
    def get_comments(self):
        return self.text_edit.toPlainText()

    # Get the status from the radio buttons
    def get_status(self):
        return self.bg_status.checkedButton().text()
