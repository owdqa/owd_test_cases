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
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': '', 'value': ''})

        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")
        
        #
        # Search for our contact.
        #
        orig_iframe = self.messages.selectAddContactButton()
        
        #
        # Search the contacts list for our contact.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for i in x:
            if i.text == self.Contact_1["name"]:
                self.UTILS.logResult("info", "Tapping ...")
                i.tap()
                break
        
        self.UTILS.waitForElements(DOM.Messages.contact_no_phones_msg, "Message saying this contact has no phones")
        x = self.UTILS.getElement(DOM.Messages.contact_no_phones_ok, "OK button")
        x.tap()
        
        self.UTILS.headerCheck("Select contact")