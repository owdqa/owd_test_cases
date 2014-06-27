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

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_2_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_2_PASS")

        self.data_layer.remove_all_contacts()

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # WIFI.
        #
        self.settings.launch()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        self.contacts.launch()
        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        cont_number = 1
        i_counter = 0
        for i in x:
            i_counter = i_counter + 1
            if "hotmail" in i.get_attribute("data-search").lower():
                cont_number = i_counter
                break

        self.contacts.import_toggle_select_contact(cont_number)
        self.marionette.execute_script("document.getElementById('{}').click()".\
                                       format(DOM.Contacts.import_import_btn[1]))

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.wait_for_element_displayed(DOM.Contacts.import_contacts_header[0], DOM.Contacts.import_contacts_header[1], timeout=10)

        self.wait_for_element_displayed(DOM.Contacts.import_contacts_back[0], DOM.Contacts.import_contacts_back[1], timeout=1)
        back = self.marionette.find_element(*DOM.Contacts.import_contacts_back)
        back.tap()

        self.wait_for_element_displayed(DOM.Contacts.settings_done_button[0], DOM.Contacts.settings_done_button[1], timeout=5)
        done = self.marionette.find_element(*DOM.Contacts.settings_done_button)
        done.tap()

        #
        # Check our two contacts are in the list.
        #
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_JSname, "Name")

        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_import, "Hotmail imported contact")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
