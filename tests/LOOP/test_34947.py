# OWD-34947: FxAccount user must be prompted to log-ing into Loop, when
# the app is executed previously but the user has logged and logout
# successfully.
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

        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")
        self.connect_to_network()

        self.loop.initial_test_checks()
        self.settings.launch()
        self.settings.fxa()
        if self.settings.is_fxa_logged_in():
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
