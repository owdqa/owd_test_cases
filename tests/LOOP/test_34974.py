#===============================================================================
# 34974: Verify ID used to log-in into Loop is not available when user is
# logged-out from loop app when has signed with MSISDN
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

        self.loop.initial_test_checks()

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
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
            time.sleep(5)
            self.loop.open_settings()
            self.loop.logout()

        # The user is not logged in, so no ID is available. The screen to authenticate
        # is shown instead
        phone_btn = self.marionette.find_element(*DOM.Loop.wizard_login_phone_number)
        self.UTILS.test.test(phone_btn, "Use phone number login button is present")
