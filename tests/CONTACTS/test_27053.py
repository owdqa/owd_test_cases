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
from OWDTestToolkit.apps.settings import Settings
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
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

        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        #
        # Check the Import button is disabled to begin with.
        #
        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Tap the Select All button (can't be done with marionette yet).
        #
        self.UTILS.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('{}').click()".\
                                       format(DOM.Contacts.import_select_all[1]))
        time.sleep(1)

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        #
        # The only way I can see to test that all contacts are selected is to toggle
        # all of them and make sure the Import button is then disabled (because that
        # means all of them were selected before the toggle).
        #
        x = self.UTILS.getElements(("class name", "block-item"), "Contacts list")
        for i in range(len(x)):
            i_num = i + 1
            self.UTILS.logResult("info", "Disable contact {} ...".format(i_num))
            self.contacts.import_toggle_select_contact(i_num)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)
