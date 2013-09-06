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
import time

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_twoPhones
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View our contact.
        #
        self.contacts.viewContact(self.cont['name'])
        
        #
        # Tap the 2nd number to dial it.
        #
        x = self.UTILS.getElement( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.cont["tel"][1]["value"]),
                                   "Second phone number")
        x.tap()
        
        #
        # Switch to the dialer iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.dialer_frame)
        
        #
        # Verify things....
        #
        time.sleep(0.5)
        x = self.UTILS.getElements(DOM.Dialer.outgoing_call_number, "Phone number")
        boolOK=False
        for i in x:
            if i.is_displayed():
                if self.cont['name'] in i.text:
                    boolOK = True
                    break
            
        self.UTILS.TEST(boolOK, "'%s' in the dialer number." % self.cont['name'])
        
        
        
        