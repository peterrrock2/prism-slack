import requests
import os
import json

from pprint import pprint

from Scripts.slack_components.blocks import SlackBlocks


# Upload a file to a channel
def upload_content(access_token, conversation_id, file, slack_user, comment):
    # Get the files size required for the upload
    file_stats = os.stat(file)
    file_size = file_stats.st_size

    try:
        # Get Slack to provide the URL used for the uploaded file
        url_request = "https://slack.com/api/files.getUploadURLExternal"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {"filename": file, "length": file_size}
        response = requests.get(url_request, headers=headers, params=payload)

    except Exception as e:
        print(f"Error getting upload URL: {e}")
        return

    # Store the URL and ID for the uploaded file
    upload_url = response.json()["upload_url"]
    id = response.json()["file_id"]

    try:
        # Upload the file to Slack
        with open(file, "rb") as f:
            files = {"file": f}
            response = requests.post(upload_url, headers=headers, files=files)

    except Exception as e:
        print(f"Error uploading the file: {e}")
        return

    finally:
        # Complete the upload process required by Slack
        post_url = "https://slack.com/api/files.completeUploadExternal"
        post_payload = {
            "files": [{"id": id, "title": file}],
            "channel_id": conversation_id,
            "initial_comment": f"Artst: <@{slack_user}>\n{comment}",
        }

        response = requests.post(post_url, headers=headers, json=post_payload)
        data = response.json()

        return data


# Post a progress message to a channel
def post_progress_message(
    access_token,
    channel,
    sequence,
    shot,
    identifier,
    version,
    slack_user,
    user_avatar,
    comment,
    status,
):
    blocks = [
        SlackBlocks().identifier_information(
            sequence, shot, identifier, version, slack_user, user_avatar, status
        ),
        SlackBlocks().comments(comment),
    ]

    if status == "Request Review":
        blocks.append(
            SlackBlocks().divider(),
        )
        blocks.append(SlackBlocks().approval_buttons())

    metadata = json.dumps(
        {
            "artist": slack_user,
        }
    )

    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"channel": channel, "blocks": blocks, "metadata": metadata}

    response = requests.post(url, headers=headers, json=payload)
    pprint(response.json())


# Post a message to a user on a channel
def post_channel_message(access_token, channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"channel": channel, "text": message}
    try:
        requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print(f"Error posting message: {e}")


# Post a direct message to a user
def post_direct_message(access_token, user_id, message):
    url = "https://slack.com/api/conversations.open"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"users": user_id}
    try:
        response = requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(f"Error opening conversation: {e}")
        return

    post_url = "https://slack.com/api/chat.postMessage"
    payload = {"channel": response.json()["channel"]["id"], "text": message}
    try:
        response = requests.post(post_url, headers=headers, json=payload)
    except Exception as e:
        print(f"Error sending direct message: {e}")


# Post an ephemeral message to a channel
def post_channel_ephemeral_message(access_token, user_id, channel_id, message):
    url = "https://slack.com/api/chat.postEphemeral"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"channel": channel_id, "user": user_id, "text": message}

    requests.post(url, headers=headers, json=payload)


# Post an ephemeral message to a user
def post_direct_ephemeral_message(access_token, user_id, message):
    url = "https://slack.com/api/conversations.open"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"users": user_id}
    try:
        response = requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print(f"Error opening conversation: {e}")
        return

    post_url = "https://slack.com/api/chat.postEphemeral"
    payload = {"channel": response.json()["channel"]["id"], "text": message}
    try:
        requests.post(post_url, headers=headers, json=payload)

    except Exception as e:
        print(f"Error sending direct ephemeral message: {e}")
