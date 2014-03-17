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

class test_main(GaiaTestCase):
    
    _newGroup = "Sports"
    
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
        self.EME.launch()
        
        #
        # Make sure our group isn't already present.
        #
        #self.EME.remove_groups([self._newGroup], p_validate=False)
        #self.EME.remove_groups([self._newGroup], p_validate=False)
        self.EME.remove_groups([self._newGroup])

        #
        # Add the group.
        #
        self.EME.add_group(self._newGroup)
            
        #
        # Remove the group.
        #
        self.EME.remove_groups([self._newGroup])
        
        
