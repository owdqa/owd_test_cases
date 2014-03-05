#
# Imports which are standard for all test cases.
#
from gaiatest   import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps import Settings
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.Settings = Settings(self)

        self.wifi_name = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

        self.hotmail_user = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.get_os_variable("HOTMAIL_1_PASS")

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # WIFI.
        #
        self.Settings.launch()

        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        self.contacts.launch()

        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # Try to get the hotmail contact (use the first one if not).
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list")
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
        time.sleep(1)

        self.apps.kill_all()
        self.contacts.launch()
        #
        # Check our contact is in the list.
        #
        self.UTILS.waitForElements(DOM.Contacts.view_all_contact_JSname, "Hotmail imported contact")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)
