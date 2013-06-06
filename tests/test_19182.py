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
import time

class test_19182(GaiaTestCase):
    _Description = "[CONTACTS] Search a contact after edit contact name."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)
                
        #
        #

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_2 = MockContacts().Contact_2
        self.data_layer.insert_contact(self.Contact_1)
        self.data_layer.insert_contact(self.Contact_2)
        self.newGivenName = "aaaaabbbbbccccaaaa"
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Change the name to "aaaaabbbbbccccaaaa"
        #
        self.contacts.changeVal(self.Contact_1['name'], "givenName", self.newGivenName)

        #
        # Search for our new contact.
        #
        self.contacts.search("aaa")
        
        #
        # Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.newGivenName, True)
        
        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.Contact_2["givenName"], False)
        
