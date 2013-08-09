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
        
        # Remove the phone number from the contact and insert it.
        self.cont = MockContacts().Contact_1
        self.cont["tel"]["type"]    = ""
        self.cont["tel"]["carrier"] = ""
        self.cont["tel"]["value"]   = ""
        self.data_layer.insert_contact(self.cont)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Add a number and add it to an existing contact.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.addThisNumberToContact(self.cont["name"])
         
        #
        # Verify that this contact has been modified in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.viewContact(self.cont["name"])
        
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Contact telephone number")
        self.UTILS.TEST(self.num in x.text, "Phone number contains %s (it was %s)." % (self.num, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot and html dump:", x)        