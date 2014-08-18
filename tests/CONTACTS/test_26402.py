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
import time


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
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
        self.test_contacts = [MockContact() for i in range(2)]

        map(self.UTILS.general.insertContact, self.test_contacts)

        self.contact_name = self.test_contacts[0]["givenName"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Go to the view details screen for this contact.
        #
        self.contacts.view_contact(self.contact_name, header_check=False)

        #
        # Tap the Send an email button.
        #
        sendEmail = self.UTILS.element.getElement(DOM.Contacts.view_contact_email_field, "Send email button")
        sendEmail.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        time.sleep(3)
        #
        # Verify a dialog appears indicating that we do not have any mail accounts configured.
        #
        x = self.UTILS.element.getElement(DOM.Email.confirm_msg,
                                   "Dialog confirmation message", True, 10, False)

        msg = "You are not set up to send or receive email. Would you like to do that now?"
        self.UTILS.test.TEST(msg == x.text,  "Verifying confirmation msg")

        #
        # Tap Ok button for confirmation.
        #
        x = self.UTILS.element.getElement(DOM.Email.confirm_ok, "OK button", True, 5, False)
        x.tap()
