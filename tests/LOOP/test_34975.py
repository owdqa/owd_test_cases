#===============================================================================
# 34975: Verify ID used to log-in into Loop is not available when user is
# logged-out from loop app when has signed with FxAccount
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit import DOM


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)

        self.connect_to_network()

        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")

        # Make sure Loop is installed
        if not self.loop.is_installed():
            self.loop.install()
        else:
            self.loop.launch()
            self.loop.open_settings()
            self.loop.logout()

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

        # The user is not logged in, so no ID is available. The screen to authenticate
        # is shown instead
        phone_btn = self.marionette.find_element(*DOM.Loop.wizard_login_phone_number)
        self.UTILS.test.TEST(phone_btn, "Use phone number login button is present")
