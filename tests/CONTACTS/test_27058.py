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
from OWDTestToolkit.apps.settings import Settings
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_2_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_2_PASS")

        self.contact = MockContact()

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

        self.contacts.import_toggle_select_contact(1)

        self.marionette.execute_script("document.getElementById('{}').click()".\
                                    format(DOM.Contacts.import_import_btn[1]))
        
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.wait_for_element_displayed(DOM.Contacts.import_contacts_header[0], DOM.Contacts.import_contacts_header[1], timeout=10)

        self.wait_for_element_displayed(DOM.Contacts.import_contacts_back[0], DOM.Contacts.import_contacts_back[1], timeout=1)
        back = self.marionette.find_element(*DOM.Contacts.import_contacts_back)
        self.UTILS.element.simulateClick(back)

        done = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Settings done button")
        self.UTILS.element.simulateClick(done)

        screen = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Before editing contact:", screen)

        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")[0]
        self.contacts.edit_contact(contact_list.text, self.contact)

        self.contacts.check_view_contact_details(self.contact)

        screen = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "After editing contact:", screen)
