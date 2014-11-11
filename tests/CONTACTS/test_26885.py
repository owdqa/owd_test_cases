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
        # Get details of our test contacts.
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
        # View the contact details.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Edit the contact.
        #
        self.contacts.press_edit_contact_button()

        #
        # Count the current email addresses.
        #
        orig_count = self.contacts.count_email_addresses_while_editing()

        #
        # Add a few email addresses.
        #
        self.contacts.add_another_email_address("one@myemail.com")
        self.contacts.add_another_email_address("two@myemail.com")

        #
        # Get the new count.
        #
        new_count = self.contacts.count_email_addresses_while_editing()

        #
        # Verify there are 3 more.
        #
        diff = (new_count - orig_count)
        self.UTILS.test.test(diff == 2,
                        "3 more emails listed for this contact before saving the changes (there were {}) .".\
                        format(diff))

        #
        # Save the changes.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Update button")
        x.tap()

        #
        # Back to 'view all' screen.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        #
        # View the contact again.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Count the email fields.
        #
        x = self.UTILS.element.getElements(DOM.Contacts.email_address_list, "Email addresses", False)
        view_count = 0
        email1_found = False
        email2_found = False
        for i in x:
            if "email-details-template-" in i.get_attribute("id"):
                view_count = view_count + 1
                btn_name = i.find_element("tag name", "button").text

                self.UTILS.reporting.logResult("info", "    - " + btn_name)
                if btn_name == "one@myemail.com":
                    email1_found = True
                if btn_name == "two@myemail.com":
                    email2_found = True

        self.UTILS.test.test(view_count == new_count, str(new_count) + " emails are displayed.")

        self.UTILS.test.test(email1_found, "First added email is present.")
        self.UTILS.test.test(email2_found, "Second added email is present.")
