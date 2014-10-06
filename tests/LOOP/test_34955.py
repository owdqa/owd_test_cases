# OWD-34955
# FxAccount user must be able to log-out from Loop, when the app is
# executed previously but the user has logged successfully.
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

        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")
        self.connect_to_network()

        # Make sure Loop is installed
        if not self.loop.is_installed():
            self.loop.install()

        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
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
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()

            header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
            self.UTILS.element.waitForElements(header, "Loop main view")

        # Now logout
        self.loop.open_settings()
        self.loop.logout()
        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")