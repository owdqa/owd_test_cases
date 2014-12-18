#===============================================================================
# 26775: Verify that user can click on any app shown by everything.me
# and launch the application
#
# Procedure:
# 1- Launch everything.me
# 2- Click on an app
#
# Expected results:
# The Application is launched correctly
#===============================================================================
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.eme = EverythingMe(self)
        self.cat_id = "207"
        self.app_name = "Pacman"

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        # Launch the group
        self.eme.pick_group(self.cat_id)
        time.sleep(3)
        pacman = self.UTILS.element.getElementByXpath(DOM.EME.app_to_install.format(self.app_name))
        pacman_url = pacman.get_attribute("data-identifier")
        self.UTILS.reporting.debug("Pacman URL: {}".format(pacman_url))
        pacman.tap()
        time.sleep(5)
        self.UTILS.iframe.switchToFrame("src", pacman_url)
        content = self.UTILS.element.getElement(DOM.EME.game_content, "Game contents")
        self.UTILS.test.test(content, "Game content found")
