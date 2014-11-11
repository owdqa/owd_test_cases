#===============================================================================
# 34981: Verify ID used to log-in into Loop is available when user has logged-in
# using Firefox Accounts. and previously has logged-in (and logged-out) with a
# MSISDN. Verify that ID is the corresponding email FxAccount
#===============================================================================

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

        self.loop.initial_test_checks()

        self.logout_fxa()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.logout_fxa()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            time.sleep(5)
            self.loop.open_settings()
            self.loop.logout()

        self.loop.launch()
        result = self.loop.wizard_or_login()
        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)

        self.UTILS.iframe.switch_to_frame(*DOM.Loop.frame_locator)
        self.loop.open_settings()
        login_info_elem = self.UTILS.element.getElement(DOM.Loop.settings_logged_as, "Login info")
        login_info = login_info_elem.text.split("\n")[-1]

        self.UTILS.test.test(login_info == self.fxa_user, "Login info matches [FxA]")

    def logout_fxa(self):
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
