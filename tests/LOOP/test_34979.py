# OWD - 34979
# Verify ID used to log-in into Loop is available  when user has logged-in
# using Firefox Accunts. Verify that ID is the corresponding email
# FxAccount
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

        # Clean start
        self.loop.launch()
        try:
            self.loop.open_settings()
            self.loop.logout()
        except:
            self.UTILS.reporting.logResult('info', "Already logged out")

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
        login_info_elem = self.UTILS.element.getElement(DOM.Loop.settings_logged_as, "Login info")
        login_info = login_info_elem.text.split("\n")[-1]

        self.UTILS.test.TEST(login_info == self.fxa_user, "Login info matches [FxA]")
