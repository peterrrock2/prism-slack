import os
import json

from Scripts.client.slack.slack_config import SlackConfig
from Scripts.client.ui.dialogs import WarningDialog, AdditionalInfoDialog

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


# Get Slack Notification User Pool from config file
def get_notify_user_pool(self):
    slack_config = self.slack_config.loadConfig("studio")

    return slack_config["slack"]["notifications"].get("user_pool")


# Get Slack Notification Method from config file
def get_notify_user_method(self):
    slack_config = self.slack_config.loadConfig("studio")

    return slack_config["slack"]["notifications"].get("method")


# Get Slack Access Token from config file
def get_access_token():
    slack_config = SlackConfig().loadConfig("studio")

    return slack_config["slack"]["token"]


# Get Slack Display Name from prism user configuration
def get_prism_slack_username(self):
    user_data = self.slack_config.loadConfig("user")

    return user_data["slack"].get("username")


# Get Slack User ID from user list
def get_slack_user_id(username, user_pool):
    for user in user_pool:
        print(user)
        if username == user["display_name"]:
            return user.get("id")

    return None


# Open dialog warning user that they are part of the team but not part of the project
def teams_user_warning(user):
    dialog = WarningDialog(team_user=user)
    if dialog.exec_() == QDialog.Accepted:
        return True
    else:
        return False


# Notify user about new version of product is on the way!
def notify_slack_user(self, access_token, slack_user, channel, product, sender):
    if os.getenv("PRISM_SEQUENCE") is not None:
        seq = os.getenv("PRISM_SEQUENCE")
        shot = os.getenv("PRISM_SHOT")

    message = self.getMessage(slack_user, seq, shot, product, sender)

    pipeline_data = self.slack_config.loadConfig("studio")
    method = pipeline_data["slack"]["notifications"].get("method")

    if method.lower() == "channel":
        self.slack_message.postChannelMessage(access_token, channel, message)
    elif method.lower() == "direct":
        self.slack_message.postDirectMessage(access_token, slack_user, message)
    elif method.lower() == "ephmeral direct":
        self.slack_message.postEphemeralDirectMessage(access_token, slack_user, message)
    else:
        self.slack_message.postChannelEphemeralMessage(
            access_token, slack_user, channel, message
        )


# Get the message to send to the user
def get_message(slack_user, seq, shot, product, sender):
    import random

    if random.randint(0, 100) == 90:
        message = f"Dearest <@{slack_user}>,\nI bring you tidings of the utmost importance! The {product} render for Shot `{shot}` in the enchanting Sequence `{seq}` has begun. Courtesy of the illustrious <@{sender}>, of course. May the pixels align in harmonious perfection!\nYours in cinematic anticipation,\nMoira Rose"

    elif random.randint(0, 100) == 100:
        message = f"<@{slack_user}>\n`{product}`/`{seq}`/`{shot}`\n<https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExeW4xNGl1dGxtMWY5d2tsMTBuYXc3enYza3FkNnpoZDNoYWlremh5NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SSiwN19NtD1xUAikqf/giphy.gif>"

    else:
        message = f"Heads up <@{slack_user}>!\n A new version of `{product}` for `{seq}`/`{shot}` is on the way!"

    return message


# Get the current project name
def get_current_project(self):
    proj = self.core.getConfig(
        "globals", "project_name", configPath=self.core.prismIni
    ).lower()

    return proj


# Get the version information from the versioninfo.json file
def get_version_info(file, mode):
    if mode == "render":
        versioninfo = os.path.dirname(os.path.dirname(file)) + "/" + "versioninfo.json"
    else:
        versioninfo = os.path.dirname(file) + "/" + "versioninfo.json"
    versioninfo = versioninfo.replace("\\", "/")

    with open(versioninfo, "r") as f:
        data = json.load(f)
        seq = data["sequence"]
        shot = data["shot"]
        identifier = data["identifier"]
        version = data["version"]

    return seq, shot, identifier, version


def getSlackComment(self):
    # Set additional comments for the upload
    info_dialog = AdditionalInfoDialog()
    if info_dialog.exec_() == QDialog.Accepted:
        comment = info_dialog.get_comments()
    else:
        self.upload_message.close()
        return

    return comment


# Upload file to Slack
def upload_to_slack(
    access_token,
    conversation_id,
    file_upload,
    sequence,
    shot,
    identifier,
    version,
    method,
):
    import time

    prism_user = get_prism_slack_username()
    channel_users = get_channel_users(access_token, conversation_id)
    slack_user = get_slack_user_id(prism_user, channel_users)

    user_avatar = get_user_avatar(access_token, slack_user)

    # Set additional comments for the upload
    info_dialog = AdditionalInfoDialog()
    if info_dialog.exec_() == QDialog.Accepted:
        comment = info_dialog.get_comments()
        status = info_dialog.get_status()
    else:
        upload_message.close()
        return

    try:
        # Upload the file to Slack
        upload = upload_content(
            access_token, conversation_id, file_upload, slack_user, comment
        )

        # if self.upload.get("ok"):
        #     file_stats = os.stat(file_upload)
        #     file_size = file_stats.st_size
        #     # Wait for upload to complete and post. Slack has a rate limit of 1MB/s
        #     delay = file_size / 1024 / 1024
        #     if delay < 2:
        #         time.sleep(2)
        #     elif delay > 20:
        #         time.sleep(20)
        #     else:
        #         time.sleep(delay)

        # Post the message to the channel
        # self.slack_message.postProgressMessage(
        #     access_token,
        #     conversation_id,
        #     sequence,
        #     shot,
        #     identifier,
        #     version,
        #     slack_user,
        #     user_avatar,
        #     comment,
        #     status,
        # )

        # Post the successful upload message
        uploaded = True
        SuccessfulPOST(uploaded, method, upload_message)

    except Exception as e:
        uploaded = False
        core.popup(f"Failed to upload file to Slack: {e}")
        SuccessfulPOST(uploaded, method, upload_message)


def publish_to_slack(self, file, seq, shot, identifier, version, mode):
    current_project = self.core.getConfig(
        "globals", "project_name", configPath=self.core.prismIni
    ).lower()

    try:
        access_token = self.get_access_token()
    except Exception as e:
        self.core.popup(
            f"Failed to retrieve Slack access token. Please check your configuration.\n\n{e}"
        )
        return

    conversation_id = get_channel_id(access_token, current_project)
    file_upload = file[0]
    file_upload.replace("\\", "/")

    upload_message = UploadDialog()
    upload_message.show()

    QTimer.singleShot(
        0,
        lambda: upload_to_slack(
            access_token,
            conversation_id,
            file_upload,
            seq,
            shot,
            identifier,
            version,
            mode,
        ),
    )


def isStudioLoaded(core):
    studio = core.plugins.getPlugin("Studio")
    return studio
