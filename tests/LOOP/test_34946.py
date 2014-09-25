# OWD-34946
# MSISDN user must be prompted to log-ing into Loop, when the app is
# executed previously but the user has logged and logout successfully.
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.connect_to_network()

        # Clean start
        if not self.loop.is_installed():
            self.loop.install()
            
        self.loop.launch()
        try:
            self.loop.open_settings()
            self.loop.logout()
        except:
            self.UTILS.reporting.logResult('info', "Already logged out")

        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()

            header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
            self.UTILS.element.waitForElements(header, "Loop main view")

        # Now logout
        self.loop.open_settings()
        self.loop.logout()

        self.apps.kill_all()
        time.sleep(2)

        # Now check for login to be prompted
        self.loop.launch()
        self.loop.wizard_or_login()

        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")
