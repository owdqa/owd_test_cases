# OWD-35813: Verify that loop user is logged-out from the app if I log-out my Firefox Account from Settings

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

        self.fxa_user = self.UTILS.general.get_config_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_config_variable("GLOBAL_FXA_PASS")

        self.connect_to_network()

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
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
        self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        # Logout and check login is prompted
        self._do_fxa_logout()

        self.loop.launch()
        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")
