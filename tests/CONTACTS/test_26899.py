#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
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
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View our contact.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Edit our contact.
        #
        self.contacts.press_edit_contact_button()

        #
        # Delete our contact.
        #
        self.contacts.press_delete_contact_button()

        #
        # Cancel deletion.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.cancel_delete_btn, "Cancel button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel edit contact")
        x.tap()

        #
        # Cancel contact edition
        #
        cancel_edition = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel edition")
        cancel_edition.tap()

        #
        # Go back to contacts start page
        #
        
        back = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back.tap()

        #
        # Now actually delete our contact.
        #
        self.contacts.delete_contact(self.contact['name'])
