#OWD-35818: Login in Loop with MSISDN - SIM introduced by user

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
        self.phone_number_without_prefix = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")[3:]

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
            self.loop.phone_login_manually(self.phone_number_without_prefix)
            self.loop.allow_permission_phone_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view") 