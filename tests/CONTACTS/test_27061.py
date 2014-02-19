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
        self.Contact_1 = MockContact()
        self.Contact_2 = MockContact()
        self.Contact_3 = MockContact()
        
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
        self.contacts.search(self.Contact_1["tel"]["value"])

        #
        # Verify that we're now in the 'search results' screen.
        #
        self.UTILS.waitForElements(DOM.Contacts.search_results_list, "Search results list")

        #
        # Cancel the search.
        #
        x = self.UTILS.getElement(DOM.Contacts.search_cancel_btn, "Cancel search button")
        x.tap()
        
        #
        # Verify that we're no longer in the 'search results' screen.
        #
        self.UTILS.waitForNotElements(DOM.Contacts.search_results_list, "Search results list")




