#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps import Settings

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
        self.contact = MockContact(tel={'type': 'Mobile', 'value': '123111111'})
        self.contact2 = MockContact(tel={'type': 'Mobile', 'value': '123222222'})
        self.contact3 = MockContact(tel={'type': 'Mobile', 'value': '133333333'})

        self.UTILS.insertContact(self.contact)
        self.UTILS.insertContact(self.contact2)
        self.UTILS.insertContact(self.contact3)

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
        self.contacts.check_search_results(self.contact["givenName"], True)
        self.contacts.check_search_results(self.contact2["givenName"], True)
        self.contacts.check_search_results(self.contact3["givenName"], False)
