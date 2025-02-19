import requests


# Get the users information
def get_user_info(access_token, user_id):
    url = "https://slack.com/api/users.info"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"user": user_id}

    try:
        response = requests.get(url, headers=headers, params=payload)
        user_info = response.json()["user"]

    except Exception as e:
        print(f"Error getting user info: {e}")
        return

    return user_info


# Get the users avatar
def get_user_avatar(access_token, user_id):
    user_info = get_user_info(access_token, user_id)

    return user_info["profile"]["image_72"]


# Get Slack Channel ID from conversation list
def get_channel_id(access_token, project_name):
    conversation_id = None

    try:
        url = "https://slack.com/api/conversations.list"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        conversations = response.json()

        for conversation in conversations["channels"]:
            if conversation["name"] == project_name:
                conversation_id = conversation["id"]
                return conversation_id

    except Exception as e:
        print(f"Error getting channel ID: {e}")
        return None


def get_team_users(access_token):
    url = "https://slack.com/api/users.list"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    members = response.json().get("members")

    team_users = []

    for m in members:
        if m.get("display_name") is not None and m.get("is_bot") == False:
            team_users.append(
                {"display_name": m.get("display_name"), "id": m.get("id")}
            )

    return team_users


# Get the Users in a Slack Channel, saving only their display name and id
def get_channel_users(access_token, conversation_id):
    url = "https://slack.com/api/conversations.members"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"channel": conversation_id}

    response = requests.get(url, headers=headers, params=params)

    channel_members = response.json()["members"]
    channel_users = []

    for m in channel_members:
        url = "https://slack.com/api/users.info"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"user": m}

        response = requests.get(url, headers=headers, params=params)

        user = response.json().get("user")

        try:
            user_name = user["profile"].get("display_name")
        except:
            user_name = user["profile"].get("real_name")

        user_id = user.get("id")

        if user.get("is_bot") == False:
            channel_users.append({"id": user_id, "display_name": user_name})

    return channel_users


def get_studio_users(core):
    studio = core.getPlugin("Studio")
    data = studio.getStudioUsers()
    users = []
    for user in data:
        if user.get("role") not in ["deactivated"]:
            users.append(user.get("name"))

    return users
