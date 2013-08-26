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
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        
        self.dialer.createMultipleCallLogEntries("1234567989", 2)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of multiple entries:", x)
        
        self.dialer.callLog_clearAll()
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of multiple entries removed:", x)
        
