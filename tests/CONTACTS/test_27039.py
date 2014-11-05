#===============================================================================
# 27039: Use the Search box to introduce characters in order to look for
# contacts
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Gmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. The list of contacts and the Search bar are shown
# 8. Tap on the Search bar (ER2)
# 9. Write some text (ER3)
#
# Expected results:
# ER1. When tapping on the Search box the corresponding keyboard is open
# ER2. It is possible to introduce text/numbers and the list is filtered
# according to that
# ER3. The list of contacts is filtering as characters are introduced
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
from gaiatest.apps.keyboard.app import Keyboard


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.keyboard = Keyboard(self.marionette)

        self.gmail_user = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.gmail_passwd = self.UTILS.general.get_os_variable("GMAIL_1_PASS")

        self.connect_to_network()
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
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        # Get the contacts.
        contact_list = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        gmail_contacts = []
        for y in contact_list:
            gmail_contacts.append(y.get_attribute("data-search"))

        search_name = gmail_contacts[0][:gmail_contacts[0].index('@')]

        #
        # Use the search bar to test ...
        #
        self.marionette.execute_script("document.getElementById('search-start').click();")

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.gmail_import_frame, via_root_frame=False)

        self.marionette.execute_script("""
        var getElementByXpath = function (path) {
            return document.evaluate(path, document, null, 9, null).singleNodeValue;
        };
        getElementByXpath("/html/body/section/section[2]/form/p/label").click();
        """)
        self.marionette.switch_to_frame()

        # Keyboard appears.
        self.UTILS.element.waitForElements(("xpath", "//iframe[contains(@{},'{}')]".\
                                    format(DOM.Keyboard.frame_locator[0], DOM.Keyboard.frame_locator[1])),
                                   "Keyboard")

        # Typing works and allows real-time filtering.
        self.UTILS.reporting.logResult("info", "Typing '{}' with the keyboard (without pressing ENTER) ...".\
                                        format(search_name))
        self.keyboard.send(search_name)

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.gmail_import_frame, via_root_frame=False)
        after_search_count = self.UTILS.element.getElements(DOM.Contacts.import_search_list, "Search list")

        self.UTILS.test.test(len(after_search_count) == 1,
                        "After typing the name '{}' the search list contains 1 contact (out of {}).".\
                        format(search_name, len(gmail_contacts)))
