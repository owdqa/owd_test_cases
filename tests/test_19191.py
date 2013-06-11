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

class test_19191(GaiaTestCase):
    _Description = "[CONTACTS] Search by text string (UPPER CASE) that matches the last name."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_2 = MockContacts().Contact_2
        self.data_layer.insert_contact(self.Contact_1)
        self.data_layer.insert_contact(self.Contact_2)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
#         x = self.UTILS.getElement(DOM.Contacts.search_field, "Search field")
#         x.tap()
#         self.keyboard.send("A")
#         self.marionette.switch_to_frame()
#         self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
#         return

        #
        # Search for our new contact.
        #
        self.contacts.search("SMITH")
        
        #
        # Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.Contact_1["givenName"], True)
        
        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.Contact_2["givenName"], False)
        
