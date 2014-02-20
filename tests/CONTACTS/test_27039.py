#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.Settings   = Settings(self)

        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

        self.gmail_u = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_p = self.UTILS.get_os_variable("GMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # WIFI.
        #
        self.Settings.launch()

        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        self.contacts.launch()
        self.contacts.import_GmailLogin(self.gmail_u, self.gmail_p)
        
        # Get the contacts.
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list")
        gmail_contacts = []
        for y in x:
            gmail_contacts.append( y.get_attribute("data-search") )

        search_name = gmail_contacts[0][:gmail_contacts[0].index('@')]

        #
        # Use the search bar to test ...
        #

        self.marionette.execute_script("document.getElementById('search-start').click();")

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.gmail_import_frame, p_viaRootFrame=False)

        self.marionette.execute_script("""
        var getElementByXpath = function (path) {
            return document.evaluate(path, document, null, 9, null).singleNodeValue;
        };
        getElementByXpath("/html/body/section/section[2]/form/p/label").click();
        """)

        self.marionette.switch_to_frame()

        # Keyboard appears.

        self.UTILS.waitForElements( ("xpath", "//iframe[contains(@%s,'%s')]" %\
                                     (DOM.Keyboard.frame_locator[0], DOM.Keyboard.frame_locator[1])),
                                   "Keyboard")

        # Typing works and allows real-time filtering.
        self.UTILS.logResult("info", "Typing '%s' with the keyboard (without pressing ENTER) ..." % search_name)
        self.keyboard.send(search_name)
        
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.gmail_import_frame, p_viaRootFrame=False)
        after_search_count = self.UTILS.getElements(DOM.Contacts.import_search_list, "Search list")

        self.UTILS.TEST(len(after_search_count) == 1, 
                        "After typing the name '%s' the search list contains 1 contact (out of %s)." %\
                        (search_name, str(len(gmail_contacts))))