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
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.dialer.callLog_addToContact(self.num, self.cont["name"])
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
         
        #
        # Re-open the call log and Verify that it now shows the contact name,
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)         
        self.UTILS.waitForElements( ("xpath", "//h1[text()='Call log']"), "Call log header")
        
        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.num),
                                   "The call log for number %s" % self.num)

        self.UTILS.TEST(self.cont["name"] in x.text, "Call log now shows '%s'." % self.cont["name"])