#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts

#
# Imports particular to this test case.
#
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
        # Prepare the contact.
        #
        self.contact = MockContact()

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.start_create_new_contact()

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.TEST(not x.is_enabled(), "Done button is not enabled")

        contFields = self.contacts.get_contact_fields()

        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replace_str(contFields['givenName'], self.contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.contact["familyName"])

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.TEST(x.is_enabled(), "Done button is not enabled")
        x.tap()

        self.contacts.view_contact(self.contact["name"])
