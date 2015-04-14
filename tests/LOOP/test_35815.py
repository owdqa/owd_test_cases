# OWD-35815: Verify that the Loop permission are shown only the first time --> Accept to share the permissions

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

        self.loop.initial_test_checks()

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
            self.loop.phone_login_auto()
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
            self.loop.phone_login_auto()
            self.UTILS.element.waitForNotElements(DOM.GLOBAL.app_permission_dialog, "Permission dialog", timeout=10)
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view", timeout=10)
