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

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.Browser   = Browser(self)
        
        #
        # Use a Gaiatest method to quickly disable cell data.
        #
        self.data_layer.disable_cell_data()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("data") == False,
                         "Data mode is disabled before we start this test.")
        
        self.UTILS.toggleViaStatusBar("data")
        
        #
        # Open the browser app. and check we can load a page.
        #
        self.Browser.launch()
        self.Browser.open_url("http://www.google.com")

        self.UTILS.toggleViaStatusBar("data")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForNotElements(DOM.Statusbar.dataConn, "Data icon in statusbar")
        
