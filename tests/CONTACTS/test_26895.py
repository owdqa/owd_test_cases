
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts


class test_main(FireCTestCase):

    email_address = "one_two@myemail.com"

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

    def tearDown(self):

        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # Click create new contact.
        self.contacts.launch()
        self.contacts.start_create_new_contact()

        # Verify that the 'DONE' button is disabled just now.
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.test.test(not done_button.is_enabled(), "Done button is disabled by default.")

        # Add some info. to the email field.
        self.UTILS.general.typeThis(DOM.Contacts.email_field, "Email field", self.email_address)

        # Verify that the 'DONE' button is enabled just now.
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.test.test(done_button.is_enabled() == True, "Done button is enabled if email is filled in.")

        # Press the DONE button and return to the view all contacts screen.
        done_button.tap()
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")

        # Verify that our contact is now present with the email address as his contact name.
        elem = (DOM.Contacts.view_all_contact_specific_contact[0],
                DOM.Contacts.view_all_contact_specific_contact[1].format(self.email_address))
        self.UTILS.element.getElement(elem, "Contact '" + self.email_address + "'")
