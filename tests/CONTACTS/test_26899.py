from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Create test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # Launch contacts app.
        self.contacts.launch()

        # View our contact.
        self.contacts.view_contact(self.contact['name'])

        # Edit our contact.
        self.contacts.press_edit_contact_button()

        # Delete our contact.
        self.contacts.press_delete_contact_button()

        # Cancel deletion.
        cancel_deletion = self.UTILS.element.getElement(DOM.Contacts.cancel_delete_btn, "Cancel button")
        cancel_deletion.tap()

        # Cancel contact edition
        self.contacts.press_cancel_edit_button()

        # Go back to contacts start page
        self.contacts.go_back_from_contact_details()

        # Now actually delete our contact.
        self.contacts.delete_contact(self.contact['name'])
