from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


# Create a dialog to let the user know whether or not the upload was successful
class SuccessfulPOST:
    def __init__(self, uploaded, method, upload_message):
        upload_message.close()

        if uploaded == True and method == "Media":
            QMessageBox.information(
                None, "Slack Upload", "Asset has been uploaded successfully"
            )
        elif uploaded == False:
            QMessageBox.warning(None, "Slack Upload", "Failed to upload asset to Slack")
        else:
            None
