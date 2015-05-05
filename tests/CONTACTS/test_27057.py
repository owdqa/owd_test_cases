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
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_config_variable("hotmail_2_email", "common")
        self.hotmail_passwd = self.UTILS.general.get_config_variable("hotmail_2_pass", "common")

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()

        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_before = len(contact_list)

        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not login_result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        frame = self.marionette.find_element(*('id', 'fb-extensions'))
        self.marionette.switch_to_frame(frame)

        self.contacts.import_toggle_select_contact(1)
        time.sleep(1)

        header_close = self.UTILS.element.getElement(DOM.Contacts.hotmail_header, "Outlook header")
        time.sleep(1)
        self.UTILS.element.simulateClickAtPos(header_close, 25, 25)

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.wait_for_element_displayed(*DOM.Contacts.import_contacts_header)
        import_header = self.marionette.find_element(*DOM.Contacts.import_contacts_header)
        time.sleep(1)
        import_header.tap(25, 25)

        done = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Settings Done button")
        time.sleep(1)
        done.tap()

        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        contacts_after = len(contact_list)

        self.UTILS.test.test(contacts_after == contacts_before,
                             "No more contacts were imported ({} before and {} after)."
                             .format(contacts_after, contacts_before))
