#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts

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
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.contact2 = MockContact()
        self.UTILS.insertContact(self.contact)
        self.UTILS.insertContact(self.contact2)

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
        self.contacts.search("XXXX")

        #
        # Verify our contact is listed.
        #
        self.contacts.check_search_results(self.contact["givenName"], False)

        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.check_search_results(self.contact2["givenName"], False)
