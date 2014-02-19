#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        
        #
        # Prepare the contact.
        #
        self.Contact_1 = MockContact()

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.startCreateNewContact()
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.TEST(not x.is_enabled(), "Done button is not enabled")
        
        contFields = self.contacts.getContactFields()
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replaceStr(contFields['givenName'  ] , self.Contact_1["givenName"])
        self.contacts.replaceStr(contFields['familyName' ] , self.Contact_1["familyName"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.TEST(x.is_enabled(), "Done button is not enabled")
        x.tap()
        
        self.contacts.viewContact(self.Contact_1["name"])