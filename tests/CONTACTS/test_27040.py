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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

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

        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        #
        # Check the Import button is disabled to begin with.
        #
        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Select / de-select contacts and make sure Import button is enabled / disabled
        # as expected.
        #
        self.UTILS.logResult("info", "Enable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Enable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Disable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Disable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)
