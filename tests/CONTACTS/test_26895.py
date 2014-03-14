#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts

class test_main(GaiaTestCase):

    email_address = "one_two@myemail.com"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Launch contacts app.
        #
        self.contacts.launch()

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Click create new contact.
        #
        self.contacts.start_create_new_contact()

        #
        # Verify that the 'DONE' button is disabled just now.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.TEST(done_button.is_enabled() == False, "Done button is disabled by default.")

        #
        # Add some info. to the email field.
        #
        self.UTILS.typeThis(DOM.Contacts.email_field, "Email field", self.email_address)

        #
        # Verify that the 'DONE' button is enabled just now.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.TEST(done_button.is_enabled() == True, "Done button is enabled if email is filled in.")

        #
        # Press the DONE button and return to the view all contacts screen.
        #
        done_button.tap()
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")

        #
        # Verify that our contact is now present with the email address as his
        # contact name.
        #
        self.UTILS.getElement(DOM.Contacts.view_all_contact_email, "Contact '" + self.email_address + "'")
