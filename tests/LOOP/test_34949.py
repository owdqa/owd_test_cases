# OWD-34949: FxAccount user must be prompted to log-ing into Loop, when
# the app is executed previously but one different FxAccount user has
# logged and logout successfully.

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

        self.fxa_user_1 = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass_1 = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")
        self.connect_to_network()

        # Clean start
        if not self.loop.is_installed():
            self.loop.install()
        else:
            self.loop.launch()
            try:
                self.loop.open_settings()
                self.loop.logout()
            except:
                self.UTILS.reporting.logResult('info', "Already logged out")

        self.settings.launch()
        self.settings.fxa()

        if self.settings.is_fxa_logged_in():
            self.settings.fxa_log_out()
        self.settings.fxa_log_in(self.fxa_user_1, self.fxa_pass_1)

        self.apps.kill_all()
        time.sleep(2)

        # First, login with the first fxa
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.tap_on_firefox_login_button()

            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            self.loop.open_settings()
            self.loop.logout()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Now logout of FxA via settings
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()

        self.apps.kill_all()
        time.sleep(2)

        # And try to login in Loop
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.tap_on_firefox_login_button()
            self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
            self.UTILS.element.waitForElements(DOM.Loop.ffox_account_login_title, "Firefox Accounts login")