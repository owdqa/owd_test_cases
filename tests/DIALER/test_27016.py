#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


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
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num})
        self.UTILS.insertContact(self.Contact_1)
        
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
         
        #
        # Open the call log and add to our contact.
        #
        self.dialer.callLog_addToContact(self.num_short, self.Contact_1["name"])

        #
        # Verify that this number was added to the contact.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.num_short),
                                    "New phone number %s in this contact" % self.num_short)