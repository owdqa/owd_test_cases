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

class test_main(GaiaTestCase):
    
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


        # Try to get the hotmail contact (use the first one if not).
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list")
        hotmail_contact = x[0].get_attribute("data-search")
        cont_number = 1
        i_counter   = 0
        for i in x:
            i_counter = i_counter + 1
            if "hotmail" in i.get_attribute("data-search").lower():
                hotmail_contact = i.get_attribute("data-search")
                cont_number = i_counter
                break
                
        self.contacts.import_toggleSelectContact(cont_number)
        
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_import_btn[1])
        time.sleep(1)
    
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Check our contact are is the list.
        #
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_all_contact_name_xpath % hotmail_contact),
                                   "Contact '%s'" % hotmail_contact)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


