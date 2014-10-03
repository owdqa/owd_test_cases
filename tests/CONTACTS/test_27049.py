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
        x = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not x or x == "ALLIMPORTED":
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        # Get the contacts.
        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        hotmail_contacts = []
        for y in x:
            hotmail_contacts.append(y.get_attribute("data-search"))

        search_name = hotmail_contacts[0]

        #
        # Use the search bar to test ...
        #
        self.marionette.execute_script("document.getElementById('search-start').click();")

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)

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
        self.UTILS.reporting.logResult("info", "Typing '{}' with the keyboard (without pressing ENTER) ...".format(search_name))
        self.keyboard.send(search_name)

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        after_search_count = self.UTILS.element.getElements(DOM.Contacts.import_search_list, "Search list")

        self.UTILS.test.TEST(len(after_search_count) == 1,
                        "After typing the name '{}' the search list contains 1 contact (out of {}).".\
                        format(search_name, len(hotmail_contacts)))
