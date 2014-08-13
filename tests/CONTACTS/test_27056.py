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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.Settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_2_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_2_PASS")

        self.data_layer.connect_to_wifi()
        
        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

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
        back.tap()

        self.wait_for_element_displayed(DOM.Contacts.settings_done_button[0], DOM.Contacts.settings_done_button[1], timeout=5)
        done = self.marionette.find_element(*DOM.Contacts.settings_done_button)
        done.tap()
        #
        # Check all our contacts are in the list.
        #
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_JSname, "Name")

        # ... and the hotmail contacts ...
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_import, "Gmail imported contact")
        self.UTILS.element.waitForElements(DOM.Contacts.view_all_contact_import2, "Hotmail imported contact")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
