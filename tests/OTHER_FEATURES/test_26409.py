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

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
    
    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.statusbar.openSettingFromStatusbar()

        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of final position:", fnam)  
   
