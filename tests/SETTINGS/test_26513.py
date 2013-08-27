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
        self.settings   = Settings(self)
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.disableAllNetworkSettings()
        
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("data") == False, "Data conn is disabled.")
        
        self.settings.launch()
        self.settings.cellular_and_data()
        x = self.UTILS.getElement( ("xpath","//a[text()='Data connection']"), "Data connection switch")
        x.tap()
        self.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON, timeout=2)
        x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
        if x.is_displayed():
            x.tap()

        self.UTILS.waitForNetworkItemEnabled("data")
        
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("data") == True, "Data conn is now enabled.")

