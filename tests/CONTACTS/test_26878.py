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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.view_contact(self.contact["name"])

        #
        # Tap the phone number.
        #
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()

        #
        # Switch to dialer.
        #
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.contact["name"])),
                                    "Outgoing call found with number matching {}".format(self.contact["name"]))

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contact:", x)
