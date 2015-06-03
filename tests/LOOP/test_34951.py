# OWD-34951:Verify when the user is previously signed in de device with
# Firefox Account, the registered email will be used as ID

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

        if not self.settings.is_fxa_logged_in():
            self.settings.fxa_log_in(self.fxa_user, self.fxa_pass)

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
            self.loop.tap_on_firefox_login_button()

            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            self.loop.open_settings()
            login_info_elem = self.UTILS.element.getElement(DOM.Loop.settings_logged_as, "Login info")
            login_info = login_info_elem.text.split("\n")[-1]
            self.UTILS.test.test(login_info == self.fxa_user, "Login info matches [FxA]")
