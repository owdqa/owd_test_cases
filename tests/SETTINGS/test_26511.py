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
        self.settings.launch()
        
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("airplane") == False, "Airplane mode is disabled by default.")
        self.UTILS.TEST(self.data_layer.get_setting('ril.radio.disabled') == False, "Radio functionality is enabled by default.")
        
        self.UTILS.logResult("info", "Turning airplane mode on ...")
        x = self.UTILS.getElement(DOM.Settings.airplane_mode_switch, "Airplane mode switch")
        x.tap()
        
        self.UTILS.waitForNetworkItemEnabled("airplane")
        
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("airplane") == True, "Airplane mode is now enabled.")
        self.UTILS.TEST(self.data_layer.get_setting('ril.radio.disabled') == True, "Radio functionality is now disabled.")