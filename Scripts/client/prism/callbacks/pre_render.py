def __init__(core, plugin):
    core.registerCallback("preRender", preRender, plugin=plugin)


def preRender(**kwargs):
    state = kwargs.get("state", None)

    try:
        access_token = get_access_token()
    except:
        core.popup(
            "Failed to retrieve Slack access token. Please check your configuration."
        )
        return

    if state.gb_slack.isChecked():
        if state.chb_slackNotify.isChecked():
            notify_user = state.cb_userPool.currentText()
            project = get_current_project()
            channel = get_channel_id(access_token, project)
            channel_users = get_channel_users(access_token, channel)
            notify_user_id = get_slack_user_id(notify_user, channel_users)
            product = state.l_taskName.text()
            sender_id = get_slack_user_id(get_prism_slack_username(), channel_users)

            notify_slack_user(access_token, notify_user_id, channel, product, sender_id)
