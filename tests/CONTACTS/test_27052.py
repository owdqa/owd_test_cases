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
from OWDTestToolkit.apps.settings import Settings
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
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.network.getNetworkConnection()

        self.contacts.launch()
        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        #
        # Check the Import button is disabled to begin with.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Select / de-select contacts and make sure Import button is enabled / disabled
        # as expected.
        #
        self.UTILS.reporting.logResult("info", "Enable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Enable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
