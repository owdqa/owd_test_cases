#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


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
        self.contacts.start_create_new_contact()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.TEST(not x.is_enabled(), "Done button is not enabled")

        contFields = self.contacts.get_contact_fields()

        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replace_str(contFields['tel'], self.contact["tel"]["value"])

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.TEST(x.is_enabled(), "Done button is not enabled")
        x.tap()

        self.contacts.view_contact(self.contact["name"])
