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
from tests.mock_data.contacts import MockContacts

class test_5976(GaiaTestCase):
    _Description = "CLONE - Press cancel button in the screen for select a contact phone number"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Import contact (adjust to the correct number).
        #
        self.Contact_twoPhones = MockContacts().Contact_twoPhones
        self.data_layer.insert_contact(self.Contact_twoPhones)
                
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
        self.messages.selectAddContactButton()
        self.contacts.search("Bobby")
        self.contacts.selectSearchResultSeveralPhones("Bobby",0)
        