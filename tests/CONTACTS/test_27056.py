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

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


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
        self.number_of_hotmail_contacts = 2

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

        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")

        self.contacts.import_all()

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.wait_for_element_displayed(DOM.Contacts.import_contacts_header[0], DOM.Contacts.import_contacts_header[1], timeout=10)

        self.wait_for_element_displayed(DOM.Contacts.import_contacts_back[0], DOM.Contacts.import_contacts_back[1], timeout=1)
        back = self.marionette.find_element(*DOM.Contacts.import_contacts_back)
        self.UTILS.element.simulateClick(back)



        self.wait_for_element_displayed(DOM.Contacts.settings_done_button[0], DOM.Contacts.settings_done_button[1], timeout=5)
        done = self.marionette.find_element(*DOM.Contacts.settings_done_button)
        self.UTILS.element.simulateClick(done)
        
        #
        # Check our three contacts are in the list.
        #
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        self.UTILS.element.waitForElements(prepopulated_contact, "Prepopulated Contact")

        # ... and the hotmail contacts ...
        hotmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))
        contacts = self.UTILS.element.getElements(hotmail_imported, "Gmail imported contacts")
        self.UTILS.test.TEST(len(contacts) == self.number_of_hotmail_contacts, "All gmail contacts has been imported")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
