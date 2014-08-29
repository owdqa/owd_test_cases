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

        #
        # We're not testing adding a contact, so just stick one
        # into the database.
        #
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Edit the contact with the new details.
        #
        self.contacts.edit_contact(self.contact["name"], self.contact2)

        #
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.check_view_contact_details(self.contact2)

        #
        # TEST: The 'edit contact' page shows the correct details for this new contact.
        #
        self.contacts.check_edit_contact_details(self.contact2)
