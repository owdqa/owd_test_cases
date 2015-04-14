#===============================================================================
# 34975: Verify ID used to log-in into Loop is not available when user is
# logged-out from loop app when has signed with FxAccount
#===============================================================================

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

        self.data_layer.connect_to_wifi()

        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.loop.initial_test_checks()
        self.logout_fxa()

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
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            time.sleep(5)
            self.loop.open_settings()
            self.loop.logout()

        # The user is not logged in, so no ID is available. The screen to authenticate
        # is shown instead
        phone_btn = self.marionette.find_element(*DOM.Loop.wizard_login_phone_number)
        self.UTILS.test.test(phone_btn, "Use phone number login button is present")

    def logout_fxa(self):
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
