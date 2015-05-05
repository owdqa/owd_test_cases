# OWD-34946
# MSISDN user must be prompted to log-ing into Loop, when the app is
# executed previously but the user has logged and logout successfully.
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
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        # Now logout
        self.loop.open_settings()
        self.loop.logout()

        self.apps.kill_all()
        time.sleep(2)

        # Now check for login to be prompted
        self.loop.launch()
        self.loop.wizard_or_login()

        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")
