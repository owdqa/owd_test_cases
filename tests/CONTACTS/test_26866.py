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
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Select a contact.
        #
        self.contacts.search(self.contact["givenName"])
        self.contacts.select_search_result(self.contact["givenName"])

        #
        # Tap on edit mode.
        #
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")
