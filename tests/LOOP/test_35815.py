# OWD-35815: Verify that the Loop permission are shown only the first time --> Accept to share the permissions

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

        # Clean start
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
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view") 

        # Logout, login, and check permissio overlay is not shown ever ever again
        self.loop.open_settings()
        self.loop.logout()

        self.apps.kill_all()
        time.sleep(2)

        self.loop.launch()
        result = self.loop.wizard_or_login()
        if result:
            self.loop.phone_login()
            self.UTILS.element.waitForNotElements(DOM.GLOBAL.app_permission_dialog, "Permission dialog", timeout=10)
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view", timeout=10)