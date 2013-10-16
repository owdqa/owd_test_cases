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
from tests._mock_data.contacts import MockContacts
import time

class test_main(GaiaTestCase):
    
    # Just to try and avoid the hotmail 'all your contacts are already imported' issue...
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)

        self.hotmail_u = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_p = self.UTILS.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
        
        self.contacts.launch()
        x = self.contacts.import_HotmailLogin(self.hotmail_u, self.hotmail_p)
        if not x or x == "ALLIMPORTED":
            self.UTILS.logResult(False, "Cannot continue past this point without importing the contacts.")
            return


        
        # Get the contacts.
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list")
        hotmail_contacts = []
        for y in x:
            hotmail_contacts.append( y.get_attribute("data-search") )

        search_name = hotmail_contacts[0]

        #
        # Use the search bar to test ...
        #

        # Keyboard appears.

        self.marionette.execute_script("document.getElementById('search-start').click();")
        #
        # self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        # self.UTILS.switchToFrame(*DOM.Contacts.hotmail_import_frame, p_viaRootFrame=False)
        #
        time.sleep(1)

        x = self.UTILS.getElement(DOM.Contacts.search_contact_input, "Search contact button")
        x.tap()

        self.marionette.switch_to_frame()
        self.UTILS.waitForElements( ("xpath", "//iframe[contains(@%s,'%s')]" %\
                                     (DOM.Keyboard.frame_locator[0], DOM.Keyboard.frame_locator[1])),
                                   "Keyboard")

        # Typing works and allows real-time filtering.
        self.UTILS.logResult("info", "Typing '%s' with the keyboard (without pressing ENTER) ..." % search_name)
        self.keyboard.send(search_name)
        
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.hotmail_import_frame, p_viaRootFrame=False)
        after_search_count = self.UTILS.getElements(DOM.Contacts.import_search_list, "Search list")

        self.UTILS.TEST(len(after_search_count) == 1, 
                        "After typing the name '%s' the search list contains 1 contact (out of %s)." %\
                        (search_name, str(len(hotmail_contacts))))