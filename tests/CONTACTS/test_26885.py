#===============================================================================
# 26885: Add multiple emails addresses
#
# Procedure:
# 1- Open Address book
# 2- Select a contact and enter in contact details
# 3- Press edit button
# 4- Press add another mail button and typing a new email address
# 5- Press add another mail button and typing a new email address
# 6- Press add another mail button and typing a new email address
#
# Expected results:
# All addresses are added
#===============================================================================

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

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)
        self.email_1 = "one@myemail.com"
        self.email_2 = "two@myemail.com"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact['name'])
        self.contacts.press_edit_contact_button()

        # Count the current email addresses.
        orig_count = self.contacts.count_email_addresses_while_editing()

        # Add a few email addresses.
        self.contacts.add_another_email_address(self.email_1)
        self.contacts.add_another_email_address(self.email_2)

        # Get the new count and check it's been updated
        new_count = self.contacts.count_email_addresses_while_editing()
        self.UTILS.test.test(new_count == orig_count + 2,
                             "After adding two email, there are three")

        update_btn = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Update button")
        update_btn.tap()
        self.contacts.go_back_from_contact_details()
        self.contacts.view_contact(self.test_contact['name'])

        # Count the email fields.
        emails_elements = self.UTILS.element.getElements(DOM.Contacts.email_address_list, "Email addresses")
        emails = [elem.find_element(*('css selector', 'button b')).text for elem in emails_elements]

        self.UTILS.test.test(self.email_1 in emails, "Email 1 has been saved")
        self.UTILS.test.test(self.email_2 in emails, "Email 2 has been saved")
