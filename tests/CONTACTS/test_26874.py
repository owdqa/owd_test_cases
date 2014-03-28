#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

#
# Imports particular to this test case.
#
from gaiatest import GaiaTestCase
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
        # Get details of our test contacts.
        #
        self.test_contacts = [MockContact() for i in range(2)]
        map(self.UTILS.general.insertContact, self.test_contacts)

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
        self.contacts.search("XXXX")

        #
        # Verify our contact is listed.
        #
        self.contacts.check_search_results(self.test_contacts[0]["givenName"], False)

        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.check_search_results(self.test_contacts[1]["givenName"], False)
