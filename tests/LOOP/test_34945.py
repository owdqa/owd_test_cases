# OWD-34945: User must be prompted to log-ing into Loop, when the app is
# executed previously but no user has ever logged successfully.

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.connect_to_network()

        self.loop.initial_test_checks()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # First, login not finished
        self.loop.launch()
        self.loop.wizard_or_login()

        self.apps.kill_all()
        time.sleep(2)

        # Now check for login to be prompted
        self.loop.launch()
        self.loop.wizard_or_login()
        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")

