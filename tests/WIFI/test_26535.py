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
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Open the Settings application.
        #
        self.Settings.launch()
           
        #
        # Tap hotspot.
        #
        self.Settings.hotSpot()

        #x = self.UTILS.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")

        x = self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/section[27]/div/ul/li/label/input").click();
            """)


        self.UTILS.TEST(x.get_attribute("disabled") != "disabled", 
                        "Hotspot settings are enabled by default (<b>signifying that 'hotspot' is off</b>).")
