#===============================================================================
# 27055: Import one contact in a non empty addressbook
#
# Pre-requisites:
# To have already some contacts on the address book.
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
# The contacts are shown fine along with the existing contacts
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

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

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)

        if not login_result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
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
        self.wait_for_element_displayed(DOM.Contacts.import_contacts_header[0], DOM.Contacts.import_contacts_header[1],
                                        timeout=10)

        self.wait_for_element_displayed(DOM.Contacts.import_contacts_back[0], DOM.Contacts.import_contacts_back[1],
                                        timeout=1)
        back = self.marionette.find_element(*DOM.Contacts.import_contacts_back)
        self.UTILS.element.simulateClick(back)

        self.wait_for_element_displayed(DOM.Contacts.settings_done_button[0], DOM.Contacts.settings_done_button[1],
                                        timeout=5)
        done = self.marionette.find_element(*DOM.Contacts.settings_done_button)
        self.UTILS.element.simulateClick(done)

        #
        # Check our two contacts are in the list.
        #
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        self.UTILS.element.waitForElements(prepopulated_contact, "Prepopulated Contact")

        hotmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))

        self.UTILS.element.waitForElements(hotmail_imported, "Hotmail imported contact")

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)
