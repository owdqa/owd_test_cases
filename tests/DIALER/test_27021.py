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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num2})
        self.UTILS.insertContact(self.Contact_1)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
         
        #
        # Open the call log and add to our contact.
        #
        self.dialer.callLog_addToContact(self.num, self.Contact_1["name"])
         
        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.num), 
                                    "Telephone number %s in contact" % self.num)
