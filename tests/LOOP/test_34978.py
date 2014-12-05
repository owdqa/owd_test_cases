#===============================================================================
# 34978: Verify ID used to log-in into Loop is available  when user has
# logged-in with MSISDN and previously has logged-in (and logged-out with
# a different FxAccount). Verify that ID is the right MSISDN number.
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
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.connect_to_network()

        self.loop.initial_test_checks()

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
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            time.sleep(5)
            self.loop.open_settings()
            self.loop.logout()

        self.loop.phone_login()
        self.loop.open_settings()
        login_info_elem = self.UTILS.element.getElement(DOM.Loop.settings_logged_as, "Login info")
        login_info = login_info_elem.text.split("\n")[-1]
        self.UTILS.reporting.logResult('info', "Login info: {}".format(login_info))
        self.UTILS.test.test(login_info == self.phone_number, "Login info matches [MSISDN]")
