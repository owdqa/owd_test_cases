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
        # View the contact details.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Edit the contact.
        #
        self.contacts.press_edit_contact_button()

        #
        # Check the items.
        #
        self.UTILS.waitForElements(DOM.Contacts.edit_update_button, "Edit 'upate' button")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot", x)
