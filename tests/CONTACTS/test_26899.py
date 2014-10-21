from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


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
        GaiaTestCase.tearDown(self)

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
        cancel_deletion = self.UTILS.element.getElement(DOM.Contacts.cancel_delete_btn, "Cancel button")
        cancel_deletion.tap()


        #
        # Cancel contact edition
        #
        cancel_edition = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel edition")
        self.UTILS.element.simulateClick(cancel_edition)

        #
        # Go back to contacts start page
        #
        
        back = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        self.UTILS.element.simulateClick(back)

        #
        # Now actually delete our contact.
        #
        self.contacts.delete_contact(self.contact['name'])
