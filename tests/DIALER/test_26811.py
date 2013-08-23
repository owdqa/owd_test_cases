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
        self.contacts   = Contacts(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        
        x = self.UTILS.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        x.tap()
    
        time.sleep(2)    
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contacts (from the dialer iframe):", x)

        self.UTILS.switchToFrame(*DOM.Dialer.contacts_sub_iframe, p_viaRootFrame=False)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contacts (from the contacts sub-iframe):", x)
