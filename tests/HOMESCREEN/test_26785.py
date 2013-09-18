#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):
    
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

        _appName = "Juegos Gratis"
        
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
        
        self.UTILS.uninstallApp(_appName)

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.EME.launch()
        x = self.EME.searchForApp(_appName)
        x.tap()

        self.marionette.switch_to_frame()
        
        self.UTILS.waitForElements(DOM.EME.launched_button_bar, "Button bar", False)
        
        x = self.UTILS.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
        x.tap()
        
        time.sleep(2)
        
        x = self.UTILS.getElement(DOM.EME.launched_button_bookmark , "Button bar - bookmark button")
        x.tap()
        
        self.marionette.switch_to_frame()
        _boolOK = False
        x = self.UTILS.getElements(DOM.EME.launched_add_to_homescreen, "Apps to be added to homescreen")
        for i in x:
            if i.text == _appName:
                i.tap()
                _boolOK = True
                break
            
        self.UTILS.TEST(_boolOK, "Adding '%s' to homescreen (app selected)." % _appName)
        
        self.UTILS.switchToFrame(*DOM.EME.add_to_home_screen_frame)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        x = self.UTILS.getElement(DOM.EME.add_to_home_screen_btn, "Add to homescreen (button)")
        x.tap()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.EME.launched_display_button_bar, "Button bar 'displayer' element")
        x.tap()
        
        x = self.UTILS.getElement(DOM.EME.launched_button_bookmark , "Button bar - bookmark button")
        self.UTILS.TEST(x.get_attribute("data-disabled") == "true", "Bookmark button is now disabled.")
        
        self.UTILS.TEST(self.UTILS.findAppIcon(_appName), "'%s' is now installed." % _appName)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of the button bar:", x)
        
        