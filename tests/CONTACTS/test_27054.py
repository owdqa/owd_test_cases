#
# Imports which are standard for all test cases.
#
from gaiatest import GaiaTestCase
#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_2_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_2_PASS")

        self.data_layer.remove_all_contacts()
        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        self.contacts.launch()

        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # Try to get the hotmail contact (use the first one if not).
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

        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header", True, 10, True)

        back = self.UTILS.element.getElement(DOM.Contacts.import_contacts_back, "Back button", True, 10, True)
        self.UTILS.element.simulateClick(back)


        done = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Done button", True, 10, True)
        self.UTILS.element.simulateClick(done)

        #
        # Check our contact is in the list.
        #
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_JSname, "Hotmail imported contact")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
