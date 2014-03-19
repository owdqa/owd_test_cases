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
import time
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
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Create the contact.
        #
        self.contacts.start_create_new_contact()
        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.contact["familyName"])

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()

        self.contacts.view_contact(self.contact["name"])

        time.sleep(1)
        self.UTILS.element.waitForNotElements(("xpath", "//h2[text()='Home']"), "'Home' section.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)
