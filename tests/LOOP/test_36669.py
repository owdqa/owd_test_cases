# Verify that the user can log-in into the app following the wizard
# (first time user uses the app) - Mobile ID

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
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.phone_login_auto()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")
