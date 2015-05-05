#===============================================================================
# 26785: Verify that an app launched from ev.me is correctly bookmarked using
# the star icon available on the bottom bar
#
# Procedure:
# 1. Go to ev.me
# 2. Launch any app
# 3. Once the app is open, go to the bottom bar an click on star icon
# 4. A dialog screen is shown giving the option to 'Add to home screen', click
# on it
#
# Expected results:
# The application is correctly bookmarked, it is added to the homescreen.
# The star icon is not available anymore for that app
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)

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
        SpreadtrumTestCase.tearDown(self)

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

        self.marionette.switch_to_frame()
        menu = self.UTILS.element.getElement(DOM.EME.launched_menu_button, "Menu button")
        menu.tap()
        add_btn = self.UTILS.element.getElement(DOM.EME.launched_add_to_homescreen, "Add to homescreen button")
        add_btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.EME.bookmark_frame_locator)
        done_btn = self.UTILS.element.getElement(DOM.EME.add_to_homescreen_done_btn, "Add Done button")
        done_btn.tap()

        self.apps.kill_all()
        time.sleep(2)

        icon = self.UTILS.app.findAppIcon(self.app_name)
        self.UTILS.test.test(icon, "Icon for application {} was found".format(self.app_name))

        time.sleep(3)
        self.UTILS.app.uninstallApp(self.app_name)
