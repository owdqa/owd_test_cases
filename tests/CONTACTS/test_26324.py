from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
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
        FireCTestCase.tearDown(self)

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
        # test: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.check_view_contact_details(self.contact2)

        #
        # test: The 'edit contact' page shows the correct details for this new contact.
        #
        self.contacts.check_edit_contact_details(self.contact2)
