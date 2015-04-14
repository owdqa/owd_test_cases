#===============================================================================
# 34805: In case mobile phone, verify the initial configured value will be the
# Front Camera.
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations


class main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        _ = setup_translations(self)

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

        self.loop.open_settings()
        selected_camera = self.marionette.find_element(*DOM.Loop.settings_selected_camera)
        front_str = _("Back camera")
        self.UTILS.test.test(selected_camera.text == front_str, "Default camera is {} (Expected: {})".\
                             format(selected_camera.text, front_str))
