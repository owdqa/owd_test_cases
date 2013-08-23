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
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.cont1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont1)
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.dialer.launch()
        self.dialer.enterNumber(self.cont1["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
        
        
        self.dialer.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.cont1["tel"]["value"]),
                           "The call log for number %s" % self.cont1["tel"]["value"])
        x.tap()
        
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)
        
        self.UTILS.waitForElements( ("xpath", "//button[contains(@class,'remark') and @data-tel='%s']" % self.cont1["tel"]["value"]),
                                     "Highlighted number")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot:", x)