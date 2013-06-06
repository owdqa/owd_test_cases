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
from marionette.keys import Keys

class test_19409(GaiaTestCase):
    _Description = "[BASIC][HOMESCREEN] Launch market installed hosted app - verify the app is launched successfully from the homescreen."
    
    APP_NAME    = 'Wikipedia'
    APP_AUTHOR  = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Market     = Market(self)
        self.Settings   = Settings(self)
        
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.UTILS.logComment("Using app '" + self.APP_NAME + "'")
        
        #
        # Ensure we have a connection.
        #
        self.UTILS.getNetworkConnection()
        
        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.uninstallApp(self.APP_NAME)
        
        #
        # Launch market app.
        #
        self.Market.launch()
                
        #
        # Install our app.
        #
        self.UTILS.TEST(self.Market.installApp(self.APP_NAME, self.APP_AUTHOR),
                        "Successfully installed application '" + self.APP_NAME + "'.", True)
                
        #
        # Launch the app from the homescreen.
        #
        self.UTILS.TEST(self.UTILS.launchAppViaHomescreen(self.APP_NAME),
                        "Application '" + self.APP_NAME + "' can be launched from homescreen.")

