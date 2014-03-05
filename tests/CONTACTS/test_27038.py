#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps import Settings

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    restart_device = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_passwd = self.UTILS.get_os_variable("GMAIL_1_PASS")

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()

        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd, False)

        #
        # Cancel the login.
        #
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Contacts.import_cancel_login, "Cancel icon")
        x.tap()

        #
        # Verify that the gmail frame is closed.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                       format(DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1])),
                                      "Gmail login frame")

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        self.UTILS.waitForElements(("xpath", "//h1[text()='Settings']"), "Settings header")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)
