# OWD-34952: Verify if the user is not signed in the device with Firefox
# Accounts, he will be redirected to the device settings application to
# sign-up into Firefox Accounts via that app.


import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


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
        self._do_fxa_logout()

    def _do_fxa_logout(self):
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.tap_on_firefox_login_button()
            self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
            self.UTILS.element.waitForElements(DOM.Loop.ffox_account_login_title, "Firefox Accounts login")
