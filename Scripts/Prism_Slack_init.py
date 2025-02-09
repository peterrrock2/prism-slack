# -----------
# Created by John Kesig while at Warm'n Fuzzy
# Contact: john.d.kesig@gmail.com

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from Scripts.prism_plugin_utils.Prism_Slack_Variables import Prism_Slack_Variables
from Scripts.prism_plugin_utils.Prism_Slack_Functions import Prism_Slack_Functions
from Scripts.prism_plugin_utils.Prism_Slack_externalAccess_Functions import (
    Prism_Slack_externalAccess_Functions,
)


class Prism_Slack(
    Prism_Slack_Variables,
    Prism_Slack_Functions,
    Prism_Slack_externalAccess_Functions,
):
    def __init__(self, core):
        Prism_Slack_Variables.__init__(self, core, self)

        self.slack_apis = os.path.join(self.pluginDirectory, "PythonLibs")
        sys.path.append(self.slack_apis)

        Prism_Slack_Functions.__init__(self, core, self)
        Prism_Slack_externalAccess_Functions.__init__(self, core, self)
