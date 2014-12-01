#===============================================================================
# 27058: Edit a contact that has been imported from Hotmail
#
# Pre-requisites:
# To have a Hotmail account with several contacts available to show/import
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. Once the list of contacts is shown, select some of them
# 8. Then tap on Import
# 9. On the address book tap on any of the imported contacts
# 10. Tap on edit option
# 11. Change/add some fields
# 12. Save the contact
# 13. Verify that the changes are saved correctly
#
# Expected results:
# It should be possible to edit a contact that has been imported from Hotmail.
# All fields imported from hotmail should also be editable.
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
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
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_config_variable("HOTMAIL_2_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_config_variable("HOTMAIL_2_PASS")

        self.contact = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.connect_to_network()

        self.contacts.launch()

        result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        self.contacts.import_toggle_select_contact(1)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Contacts Import button")
        self.UTILS.element.simulateClick(import_btn)

        self.UTILS.iframe.switch_to_frame(*DOM.Contacts.frame_locator)
        self.wait_for_element_displayed(*DOM.Contacts.import_contacts_header, timeout=10)

        self.wait_for_element_displayed(*DOM.Contacts.import_contacts_back, timeout=1)
        back = self.marionette.find_element(*DOM.Contacts.import_contacts_back)
        self.UTILS.element.simulateClick(back)

        done = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Settings done button")
        self.UTILS.element.simulateClick(done)

        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")[0]
        self.contacts.edit_contact(contact_list.text, self.contact)

        self.contacts.check_view_contact_details(self.contact)
