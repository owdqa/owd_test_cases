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

        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()

        self.UTILS.switchToFrame(*DOM.Home.frame_locator)

        #
        # Launch the group
        #
        self.EME.pickGroup("Games")
        
        self.EME.launchFromGroup("Juegos Gratis")