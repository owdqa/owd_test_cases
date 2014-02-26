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
        self.contacts   = Contacts(self)
        
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': '123111111'})
        self.Contact_2 = MockContact(tel = {'type': 'Mobile', 'value': '123222222'})
        self.Contact_3 = MockContact(tel = {'type': 'Mobile', 'value': '133333333'})

        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.insertContact(self.Contact_2)
        self.UTILS.insertContact(self.Contact_3)

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
        self.contacts.search("12")
        
        #
        # Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.Contact_1["givenName"], True)
        self.contacts.checkSearchResults(self.Contact_2["givenName"], True)
        self.contacts.checkSearchResults(self.Contact_3["givenName"], False)
