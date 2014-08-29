#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
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
        self.test_contacts = [MockContact() for i in range(2)]
        map(self.UTILS.general.insertContact, self.test_contacts)
        self.new_given_name = "aaaaabbbbbccccaaaa"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.network.getNetworkConnection()

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Change the name to "aaaaabbbbbccccaaaa"
        #
        self.contacts.change_contact(self.test_contacts[0]['name'], "givenName",
                                    self.new_given_name)

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
        self.contacts.check_search_results(self.test_contacts[1]["givenName"], False)
