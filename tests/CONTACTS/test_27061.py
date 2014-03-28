#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Create our test contacts.
        #
        self.contact_list = [MockContact() for i in range(3)]
        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.search(self.contact_list[0]["tel"]["value"])

        #
        # Verify that we're now in the 'search results' screen.
        #
        self.UTILS.element.waitForElements(DOM.Contacts.search_results_list, "Search results list")

        #
        # Cancel the search.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.search_cancel_btn, "Cancel search button")
        x.tap()

        #
        # Verify that we're no longer in the 'search results' screen.
        #
        self.UTILS.element.waitForNotElements(DOM.Contacts.search_results_list, "Search results list")
