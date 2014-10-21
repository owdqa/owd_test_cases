#===============================================================================
# 27049: Use the Search box to introduce characters in order to look for contacts
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. The list of contacts and the Search bar are shown
# 8. Tap on the Search bar (ER2)
# 9. Write some text (ER3)
#
# Expected results:
# ER1. When tapping on the Search box the corresponding keyboard is open
# ER2. It is possible to introduce text/numbers in the Search box
# ER3. The list is filtered according to that introduced in the Search box
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    # Just to try and avoid the hotmail 'all your contacts are already imported' issue...
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
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
        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not login_result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # Get the contacts.
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        contact_list = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        hotmail_contacts = []
        for contact in contact_list:
            hotmail_contacts.append(self.marionette.find_element('css selector', 'strong', contact.id).text)

        search_name = hotmail_contacts[0]
        self.UTILS.reporting.debug("*** Hotmail contacts: {}".format(hotmail_contacts))

        #
        # Use the search bar to test ...
        #
        search_field = self.UTILS.element.getElement(DOM.Contacts.search_field, "Search field")
        self.UTILS.element.simulateClick(search_field)
        
        search_input = self.UTILS.element.getElement(DOM.Contacts.search_contact_input, "Search Contact input")
        self.UTILS.element.simulateClick(search_input)

        self.marionette.switch_to_frame()
        self.wait_for_element_displayed('css selector', 'iframe[src*=keyboard]', timeout=15)
        keyboard = self.marionette.find_element('css selector', 'iframe[src*=keyboard]')
        self.UTILS.test.TEST(keyboard, "ER1: Keyboard found after tapping search input")
        keyboard.send_keys(search_name)

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        search_input = self.UTILS.element.getElement(DOM.Contacts.search_contact_result_input,
                                                     "Search Contact results input")
        self.UTILS.test.TEST(search_input.get_attribute("value") == search_name, "ER2: Text and numbers in search box")

        after_search_count = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Search list")

        self.UTILS.test.TEST(len(after_search_count) == 1,
                        "ER3: After typing the name '{}' the search list contains 1 contact (out of {}).".\
                        format(search_name, len(hotmail_contacts)))
