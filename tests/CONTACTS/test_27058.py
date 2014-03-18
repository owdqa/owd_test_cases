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

        self.hotmail_user = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.get_os_variable("HOTMAIL_1_PASS")

        self.contact = MockContact()

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

        self.contacts.import_toggle_select_contact(1)

        self.marionette.execute_script("document.getElementById('{}').click()".\
                                    format(DOM.Contacts.import_import_btn[1]))
        time.sleep(1)

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Before editing contact:", x)

        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")[0]
        self.contacts.editContact(x.text, self.contact)

        self.contacts.check_view_contact_details(self.contact)

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "After editing contact:", x)
