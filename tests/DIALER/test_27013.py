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



class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
        # Remove the phone number from the contact and insert it.
        self.Contact_1 = MockContact(tel = {'type': '', 'value': ''})
        self.UTILS.insertContact(self.Contact_1)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Add a number and add it to an existing contact.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.addThisNumberToContact(self.Contact_1["name"])
         
        #
        # Verify that this contact has been modified in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Contact telephone number")
        self.UTILS.TEST(self.num in x.text, "Phone number contains %s (it was %s)." % (self.num, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot and html dump:", x)        