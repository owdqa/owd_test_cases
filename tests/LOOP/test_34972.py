#===============================================================================
# 34972: Verify ID used to log-in into Loop is not available when user is not
# logged in Loop app.
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

        # The user is not logged in, so no ID is available. The screen to authenticate
        # is shown instead
        ffox_btn = self.marionette.find_element(*DOM.Loop.wizard_login_ffox_account)
        self.UTILS.test.test(ffox_btn, "Use Firefox Accounts login button is present")
