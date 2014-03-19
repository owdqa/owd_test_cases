#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.dialer     = Dialer(self)

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.viewContact(self.Contact_1["name"])

        #
        # Tap the phone number.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()

        #
        # Switch to dialer.
        #
        _warn = self.UTILS.element.getElement( ("xpath", "//p[contains(text(), 'airplane mode')]"), 
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Airplane mode warning displayed: \"%s\"" % _warn.text, x)

        x = self.UTILS.element.getElement( ("xpath", "//button[text()='OK']"), "OK button")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Contacts.view_details_title, "Contact details")