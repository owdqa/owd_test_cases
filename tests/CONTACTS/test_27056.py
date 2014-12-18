#===============================================================================
# 27056: Import all contacts at once
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
# 7. Once the list of contacts is shown, tap on Select all
# 8. Then tap on Import
#
# Expected results:
# All Hotmail contacts are selected and after tapping on import, successfully
# imported into the address book
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

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.hotmail_user = self.UTILS.general.get_config_variable("hotmail_2_email", "common")
        self.hotmail_passwd = self.UTILS.general.get_config_variable("hotmail_2_pass", "common")
        self.number_of_hotmail_contacts = 2

        self.data_layer.connect_to_wifi()

        # Create test contacts.
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
        self.contacts.import_all()

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

        # Check our three contacts are in the list.
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        self.UTILS.element.waitForElements(prepopulated_contact, "Prepopulated Contact")

        # ... and the hotmail contacts ...
        hotmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))
        contacts = self.UTILS.element.getElements(hotmail_imported, "Gmail imported contacts")
        self.UTILS.test.test(len(contacts) == self.number_of_hotmail_contacts, "All gmail contacts has been imported")

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)
