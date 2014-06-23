#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
    _GROUP_NAME  = "Games"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)

        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        #
        # Ensure we have a connection
        #
        self.connect_to_network()
        
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")


    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
 
        #
        # First, get the name of the app we're going to install.
        #

        self.UTILS.test.TEST(self.EME.pick_group(self._GROUP_NAME),
                        "Group '" + self._GROUP_NAME + "' exists in EverythingME.",
                        True)
 
        x = self.UTILS.element.getElements(DOM.EME.app_to_install, "The first game that is not installed already")[0]
        self._APP_NAME = x.get_attribute("data-name")
        self.UTILS.home.goHome()

        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.app.uninstallApp(self._APP_NAME)
    
        #
        # Launch the 'everything.me' app.
        #
        self.EME.launch()

        #
        # Pick a group.
        #
        self.EME.pick_group(self._GROUP_NAME)

        #
        # Add the app to the homescreen.
        #
        self.UTILS.test.TEST(self.EME.add_app_to_homescreen(self._APP_NAME),
                        "Application '" + self._APP_NAME + "' is added to the homescreen.",
                        True)

        self.UTILS.home.goHome()

        #
        # Check if message is here and app was installed.
        #
        self.UTILS.app.isAppInstalled(self._APP_NAME)
