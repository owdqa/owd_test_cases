#===============================================================================
# 34786: Review the initial configured value will be Video for a device with at
# least one camera.
#===============================================================================

import sys
sys.path.insert(1, "./")
import time
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

        self.connect_to_network()

        # Clean start
        if not self.loop.is_installed():
            self.loop.install()

        self.loop.launch()
        try:
            self.loop.open_settings()
            self.loop.logout()
        except:
            self.UTILS.reporting.logResult('info', "Already logged out")

        self.apps.kill_all()
        time.sleep(2)
        _ = setup_translations(self)

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

        # Now logout
        self.loop.open_settings()
        cameras = self.marionette.find_element(*DOM.Loop.settings_select_camera)
        options = cameras.find_elements('css selector', 'option')
        if len(options) > 0:
            self.UTILS.reporting.debug("*** Found {} options for camera".format(len(options)))
            default_mode = self.marionette.find_element(*DOM.Loop.settings_selected_call_mode)
            self.UTILS.reporting.debug("*** Default call mode: {}".format(default_mode.text))
            video_str = _("Video")
            self.UTILS.test.TEST(default_mode.text == video_str, "Default call mode is {} (Expected: {})".\
                                 format(default_mode.text, video_str))
        else:
            self.UTILS.reporting.debug("No camera detected")
