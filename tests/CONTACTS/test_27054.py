#===============================================================================
# 27054: Import one contact in an empty addressbook
#
# Pre-requisites:
# Do not have any contacts on the address book.
# To have a Hotmail account with several contacts available to show/import
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. Once the list of contacts is shown, select one of the contacts
# 8. Tap on Import
#
# Expected results:
# The contacts is successfully imported into the user's address book.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

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
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.contacts.launch()

        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not login_result or login_result == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # Try to get the hotmail contact (use the first one if not).
        contact_list = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        cont_number = 1
        i_counter = 0
        for i in contact_list:
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
        hotmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))

        self.UTILS.element.waitForElements(hotmail_imported, "Hotmail imported contact")

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)
