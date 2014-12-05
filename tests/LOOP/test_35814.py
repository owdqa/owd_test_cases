# OWD-35814: Verify that if Firefox Account password is invalid the user is not logged-in in the app

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)
        _ = setup_translations(self)

        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_fake_pass = "You_shall_not_pass"
        self.expected_error_msg = _("Invalid Password")

        self.connect_to_network()

        self.loop.initial_test_checks()

        # Make sure we're not already logged in
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
            self.loop.firefox_login(self.fxa_user, self.fxa_fake_pass, is_wrong=True)

            # We're informed of a wrong log in
            self.UTILS.element.waitForElements(DOM.Loop.ffox_account_error_overlay, "Error overlay")
            error_msg = self.UTILS.element.getElement(DOM.Loop.ffox_account_error_overlay_title, "Error overlay title")
            self.UTILS.test.test(error_msg.text == self.expected_error_msg, "Invalid password message is shown")
            self.UTILS.element.waitForNotElements(DOM.Loop.app_header, "Loop main view")
