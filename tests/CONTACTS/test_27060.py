#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
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

        #
        # Get details of our test contacts.
        #
        self.phones = ["123111111", "123222222", "133333333"]

        self.test_contacts = [MockContact(tel={'type': 'Mobile', 'value': self.phones[i]})\
                                for i in range(3)]
        map(self.UTILS.insertContact, self.test_contacts)

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
        conditions = [True, True, False]
        names = [c["givenName"] for c in self.test_contacts]
        map(self.contacts.check_search_results, names, conditions)
