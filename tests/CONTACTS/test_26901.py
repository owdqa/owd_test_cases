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
        self.settings = Settings(self)

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.contact2 = MockContact()
        self.UTILS.insertContact(self.contact)
        self.UTILS.insertContact(self.contact2)
        self.new_given_name = "aaaaabbbbbccccaaaa"

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
        self.contacts.change_contact(self.contact['name'], "givenName", self.new_given_name)

        #
        # Search for our new contact.
        #
        self.contacts.search("aaa")

        #
        # Verify our contact is listed.
        #
        self.contacts.check_search_results(self.new_given_name, True)

        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.check_search_results(self.contact2["givenName"], False)
