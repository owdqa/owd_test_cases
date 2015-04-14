#===============================================================================
# 34981: Verify ID used to log-in into Loop is available when user has logged-in
# using Firefox Accounts. and previously has logged-in (and logged-out) with a
# MSISDN. Verify that ID is the corresponding email FxAccount
#===============================================================================

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.decorators import retry


class main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.data_layer.connect_to_wifi()

        self.loop.initial_test_checks()

        self.logout_fxa()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.logout_fxa()
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            time.sleep(5)
            self.loop.open_settings()
            self.loop.logout()

        # self.loop.launch()
        result = self.loop.wizard_or_login()
        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            
        self.UTILS.iframe.switch_to_frame(*DOM.Loop.frame_locator)
        self.loop.open_settings()
        login_info_elem = self.UTILS.element.getElement(DOM.Loop.settings_logged_as, "Login info")
        login_info = login_info_elem.text.split("\n")[-1]

        self.UTILS.test.test(login_info == self.fxa_user, "Login info matches [FxA]")

    def logout_fxa(self):
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
