import os


def __init__(core):
    core = core
    core.registerCallback(
        "mediaPlayerContextMenuRequested",
        mediaPlayerContextMenuRequested,
        plugin=plugin,
    )


def mediaPlayerContextMenuRequested(core, origin, menu):
    if not type(origin.origin).__name__ == "MediaBrowser":
        return

    identifier = origin.origin.getCurrentIdentifier()["identifier"]
    sequence = origin.origin.getCurrentIdentifier()["sequence"]
    shot = origin.origin.getCurrentIdentifier()["shot"]
    version = origin.origin.getCurrentVersion()["version"]

    action = QAction("Publish to Slack", origin)
    iconPath = os.path.join(pluginDirectory, "Resources", "slack-icon.png")
    icon = core.media.getColoredIcon(iconPath)

    action.triggered.connect(
        lambda: publish_to_slack(
            origin.seq,
            sequence,
            shot,
            identifier,
            version,
            mode="Media",
        )
    )

    menu.insertAction(menu.actions()[-1], action)
    action.setIcon(icon)


def mediaPlayerContextMenuRequested(core):
    def inner_func(origin, menu):
        if not type(origin.origin).__name__ == "MediaBrowser":
            return

        identifier = origin.origin.getCurrentIdentifier()["identifier"]
        sequence = origin.origin.getCurrentIdentifier()["sequence"]
        shot = origin.origin.getCurrentIdentifier()["shot"]
        version = origin.origin.getCurrentVersion()["version"]

        action = QAction("Publish to Slack", origin)
        iconPath = os.path.join(pluginDirectory, "Resources", "slack-icon.png")
        icon = core.media.getColoredIcon(iconPath)

        action.triggered.connect(
            lambda: publish_to_slack(
                origin.seq,
                sequence,
                shot,
                identifier,
                version,
                mode="Media",
            )
        )

        menu.insertAction(menu.actions()[-1], action)
        action.setIcon(icon)

    return inner_func
