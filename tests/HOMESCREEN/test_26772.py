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
        self.actions    = Actions(self.marionette)
        
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
    
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
         
        #
        # First, get the name of the app we're going to install.
        #
        self.EME.launch()
        
        self.EME.pickGroup("Games")
        
        #
        # Get the name of the first app which is installed (it'll be in the first apps listed).
        #
        x = self.UTILS.getElements(DOM.EME.apps_installed, "Installed apps in 'Games' group")[0]
        _appName = x.get_attribute("data-name")
        self.actions.press(x).wait(2).release().perform()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_alert_msg, "Alert message")
        self.UTILS.TEST(_appName in x.text, "Alert ('%s') contains '%s'." % (x.text, _appName))
        
        x = self.UTILS.getElement(DOM.GLOBAL.modal_alert_ok, "OK button")
        x.tap()
        