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
import time

class test_main(GaiaTestCase):

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
        self.cont1 = MockContacts().Contact_1
        self.cont2 = MockContacts().Contact_2
        
        self.cont1["givenName"] = self.cont1["tel"]["value"]
        self.cont2["familyName"] = self.cont2["tel"]["value"]
        
        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.UTILS.logResult("info", "<b>Search against number in 'given name' field ...</b>")
        self.contacts.search(self.cont1["tel"]["value"])
        self.contacts.checkSearchResults(self.cont1["givenName"])
        
        x = self.UTILS.getElement(DOM.Contacts.search_cancel_btn, "Search cancel button")
        x.tap()

        self.UTILS.logResult("info", "<b>Search against number in 'family name' field ...</b>")
        self.contacts.search(self.cont2["tel"]["value"])
        self.contacts.checkSearchResults(self.cont2["givenName"])
