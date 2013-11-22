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
        
        self.num        = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num_short  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        
        # Remove the phone number from the contact and insert it.
        self.cont = MockContacts().Contact_1
        self.cont["tel"]["value"]   = self.num
        self.data_layer.insert_contact(self.cont)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num_short)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        time.sleep(2)
        x = self.UTILS.getElement(DOM.Dialer.call_busy_button_ok, "OK button (Number is busy)")
        x.tap()
         
        #
        # Open the call log and add to our contact.
        #
        self.dialer.callLog_addToContact(self.num_short, self.cont["name"])

        #
        # Verify that this number was added to the contact.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.cont["name"])
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.num_short),
                                    "New phone number %s in this contact" % self.num_short)