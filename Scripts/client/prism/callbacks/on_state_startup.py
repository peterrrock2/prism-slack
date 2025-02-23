from Scripts.client.slack.api import get_channel_users, get_team_users, get_studio_users
from Scripts.client.prism.ui.state_manager_ui import StateManagerUI


def __init__(self, core):
    core = core
    core.registerCallback("onStateStartup", self.onStateStartup, plugin=self)


def onStateStartup(self, state):
    # Add Slack publishing options to the State Manager
    if state.className == "Playblast":
        lo = state.gb_playblast.layout()
    elif state.className == "ImageRender":
        lo = state.gb_imageRender.layout()
    else:
        return

    if not hasattr(state, "gb_slack"):
        state.gb_slack = QGroupBox()
        state.gb_slack.setTitle("Slack")
        state.gb_slack.setCheckable(True)
        state.gb_slack.setChecked(False)
        state.gb_slack.setObjectName("gb_slack")
        state.gb_slack.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.lo_slack_group = QVBoxLayout()
        self.lo_slack_group.setContentsMargins(-1, 15, -1, -1)
        state.gb_slack.setLayout(self.lo_slack_group)

        lo.addWidget(state.gb_slack)

    state.gb_slack.toggled.connect(
        lambda toggled: self.create_slack_submenu(toggled, state)
    )


def createSlackSubmenu(toggled, state):
    try:
        state_manager_ui = StateManagerUI(core)
        # If the group box is toggled on
        if toggled:
            if not hasattr(state, "cb_userPool"):
                state_manager_ui.createStateManagerSlackUI(state)
                populateUserPool(state)
        else:
            layout = state.gb_slack.layout()
            state_manager_ui.removeCleanupLayout(layout, "lo_slack_publish", state)
            state_manager_ui.removeCleanupLayout(layout, "lo_slack_notify", state)
    except Exception as e:
        print(f"Error creating Slack submenu: {e}")


def populateUserPool(state):
    try:
        access_token = get_access_token()
        proj = get_current_project()
        channel_id = get_channel_id(access_token, proj)

        notify_user_pool = get_notify_user_pool().lower()
        users = []
        if notify_user_pool == "studio":
            users = get_studio_users()

        elif notify_user_pool == "channel":
            members = get_channel_users(access_token, channel_id)
            users = [member["display_name"] for member in members]

        elif notify_user_pool == "team":
            members = get_team_users(access_token)
            users = [member["display_name"] for member in members]

        state.cb_userPool.addItems(users)

    except Exception as e:
        print(f"Failed to populate user pool: {e}")
