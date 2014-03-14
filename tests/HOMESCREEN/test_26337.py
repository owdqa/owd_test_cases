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
from OWDTestToolkit.apps.marketplace import Marketplace
from OWDTestToolkit.apps import Settings


class test_main(GaiaTestCase):
    
    APP_NAME    = 'Wikipedia'
    APP_AUTHOR  = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Market     = Marketplace(self)
        self.Settings   = Settings(self)
        
    def tearDown(self):
#         self.messages.waitForSMSNotifier("222000",5)
#         self.UTILS.clearAllStatusBarNotifs()

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

