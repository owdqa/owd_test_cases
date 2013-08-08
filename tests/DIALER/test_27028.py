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
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.num, 2)
         
        #
        # Add to our contact.
        #
        self.dialer.callLog_addToContact(self.num, self.cont["name"], p_openCallLog=False)
         
        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.cont["name"])
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.num), 
                                    "Telephone number %s in conact" % self.num)
