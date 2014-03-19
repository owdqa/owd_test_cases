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
        # Create our test contacts.
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

        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_before = len(x)

        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        self.contacts.import_toggle_select_contact(1)

        # El.tap() not working on this just now.
        self.marionette.execute_script("document.getElementById('{}').click()".\
                                       format(DOM.Contacts.import_close_icon[1]))

        time.sleep(1)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        x = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Settings done button")
        x.tap()

        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_after = len(x)

        self.UTILS.test.TEST(contacts_after == contacts_before, "No more contacts were imported ({} before and {} after)."\
                        .format(contacts_after, contacts_before))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "x", x)
