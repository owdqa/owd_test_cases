#===============================================================================
# 26352: Install and launch an everything.me app - verify the
# everything.me app launches successfully to the right web content
#
# Procedure:
# 1- Open Settings app and select cellular and data option
# 2- Activate data connection
# ER1
# 3- Press home button and open everything.me (swiping right)
# 4- Open a category
# 5- Long tap an app
# 6- Press OK
# ER2
# 7- Open the installed app
# ER3
#
# Expected results:
# ER1 Data connection is activated
# ER2 The app is installed and shows the correct icon
# ER3 The app is launched successfully
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
import time


class test_main(FireCTestCase):

    _group_name = "Games"
    _group_games_id = "207"

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)

        #
        # Don't prompt me for geolocation
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        #
        # First, get the name of the app we're going to install.
        #
        time.sleep(3)
        found = self.EME.pick_group(self._group_games_id)
        self.UTILS.reporting.debug("*** Group found: {}".format(found))
        self.UTILS.test.test(found, "Group '{}' exists in EverythingME.".format(self._group_name), True)

        self.UTILS.iframe.switchToFrame(*DOM.EME.frame_locator)
        app_name = self.UTILS.element.getElementByXpath(DOM.EME.app_to_install.format("Pacman")).text
        self.UTILS.reporting.logResult("info", "App name is <b>{}</b>".format(app_name))
        self.UTILS.home.goHome()

        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.app.uninstallApp(app_name)

        #
        # Pick a group.
        #
        found = self.EME.pick_group(self._group_games_id)
        self.UTILS.test.test(found, "Group '{}' exists in EverythingME.".format(self._group_name), True)
        time.sleep(2)

        #
        # Add the app to the homescreen.
        #
        added = self.EME.add_app_to_homescreen(app_name)

        self.UTILS.iframe.switchToFrame(*DOM.EME.bookmark_frame_locator)
        time.sleep(4)
        url = self.UTILS.element.getElement(DOM.EME.bookmark_url, "Bookmark_url").get_attribute("value")
        self.UTILS.reporting.debug("**** URL: {}".format(url))
        add_btn = self.UTILS.element.getElement(DOM.EME.add_bookmark_btn, "Add bookmark to Home Screen Button")
        add_btn.tap()

        self.UTILS.test.test(added, "Application '{}' is added to the homescreen.".format(app_name), True)

        #
        # Go back to the homescreen and check it's installed.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
        self.UTILS.test.test(self.UTILS.app.launchAppViaHomescreen(app_name), app_name + " is installed.", True)

        #
        # Give it 10 seconds to start up, switch to the frame for it and grab a screenshot.
        #
        time.sleep(3)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame("src", url)

        x = self.UTILS.debug.screenShot(app_name)
        self.UTILS.reporting.logResult("info", "NOTE: For a screenshot of the game running, please see this: " + x)
