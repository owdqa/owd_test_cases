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
        # Create test contacts.
        #
        self.contact_list = [MockContact() for i in range(3)]
        map(self.UTILS.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for the sought contact.
        #
        self.UTILS.logResult("info", "<b>Search against number in 'given name' field ...</b>")
        self.contacts.search(self.contact_list[1]["tel"]["value"])
        self.contacts.check_search_results(self.contact_list[1]["givenName"])
