#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts


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
        self.cont1 = MockContacts().contact
        self.cont2 = MockContacts().contact2

        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)

        self.contact_name = self.cont1["givenName"]

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Go to the view details screen for this contact.
        #
        self.contacts.view_contact(self.contact_name, p_HeaderCheck=False)

        #
        # Tap the Send an email button.
        #
        sendEmail = self.UTILS.getElement(DOM.Contacts.view_contact_email_field, "Send email button")
        sendEmail.tap()

        #
        # Verify a dialog appears indicating that we do not have any mail accounts configured.
        #
        self.marionette.switch_to_frame()

        #
        # Tap Ok button for confirmation.
        #
        x = self.UTILS.getElement(DOM.GLOBAL.modal_confirm_ok, "OK button", True, 5, False)
        x.tap()
