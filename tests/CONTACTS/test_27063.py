#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
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
        self.contact = MockContact(givenName='1111111')
        self.contact2 = MockContact(familyName='2222222')

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
        self.UTILS.logResult("info", "<b>Search against number in 'given name' field ...</b>")
        self.contacts.search('1111111')
        self.contacts.check_search_results(self.contact["givenName"])

        x = self.UTILS.getElement(DOM.Contacts.search_cancel_btn, "Search cancel button")
        x.tap()

        self.UTILS.logResult("info", "<b>Search against number in 'family name' field ...</b>")
        self.contacts.search('2222222')
        self.contacts.check_search_results(self.contact2["givenName"])
