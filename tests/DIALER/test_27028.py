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
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
        self.Contact_1 = MockContact()
        self.UTILS.insertContact(self.Contact_1)
        
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
        self.dialer.callLog_addToContact(self.num, self.Contact_1["name"], p_openCallLog=False)
         
        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_contact_tels_xpath % self.num), 
                                    "Telephone number %s in conact" % self.num)
