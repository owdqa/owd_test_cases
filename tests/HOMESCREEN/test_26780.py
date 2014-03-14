#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.setPermission('Homescreen', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):    
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        
        #
        # Make sure our group isn't already present.
        #
        self.EME.pick_group("Games")

        x = self.UTILS.getElements(DOM.EME.app_to_install, "Installed apps in 'Games' group")[0]
        x.tap()

        self.marionette.switch_to_frame()
        
        self.UTILS.waitForElements(DOM.EME.launched_button_bar, "Button bar", False)
        
        x = self.UTILS.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
        x.tap()

        self.UTILS.waitForElements(DOM.EME.launched_button_back     , "Button bar - back button")
        self.UTILS.waitForElements(DOM.EME.launched_button_forward  , "Button bar - forward button")
        self.UTILS.waitForElements(DOM.EME.launched_button_reload   , "Button bar - reload button")
        self.UTILS.waitForElements(DOM.EME.launched_button_bookmark , "Button bar - bookmark button")
        self.UTILS.waitForElements(DOM.EME.launched_button_close    , "Button bar - close button")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of the button bar:", x)