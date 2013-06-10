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
import time

class test_19354(GaiaTestCase):
    _Description = "[UTILITY TRAY] Open settings app from utility tray."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.openSettingFromStatusbar()
        
        self.UTILS.screenShotOnErr()
        
