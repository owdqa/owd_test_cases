#===============================================================================
# 27057: Tap on Cancel ('x') option after selecting some contacts
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
# 7. Once the list of contacts is shown select several of them
# 8. Tap on Cancel ('x') option
#
# Expected results:
# User is taken back to Contact settings without importing any contact
#===============================================================================

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
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

        #
        # Create our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.connect_to_network()

        self.contacts.launch()

        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_before = len(contact_list)

        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not login_result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        self.contacts.import_toggle_select_contact(1)

        time.sleep(1)
        self.wait_for_element_displayed(*DOM.Contacts.import_import_btn, timeout=10)

        self.wait_for_element_displayed(*DOM.Contacts.import_close_icon, timeout=1)
        close = self.marionette.find_element(*DOM.Contacts.import_close_icon)
        self.UTILS.element.simulateClick(close)

        self.UTILS.iframe.switch_to_frame(*DOM.Contacts.frame_locator)
        back = self.UTILS.element.getElement(DOM.Contacts.import_contacts_back, "Import Back button")
        back.tap()
        time.sleep(2)
        done = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Settings Done button")
        done.tap()
        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_after = len(contact_list)

        self.UTILS.test.TEST(contacts_after == contacts_before,
                             "No more contacts were imported ({} before and {} after)."\
                             .format(contacts_after, contacts_before))
