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
        
        self.cont = MockContacts().Contact_1

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

        self.contacts.import_toggleSelectContact(1)
        
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_import_btn[1])
        time.sleep(1)

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Before editing contact:", x)
        
        
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")[0]
        self.contacts.editContact(x.text, self.cont)
        
        self.contacts.checkViewContactDetails(self.cont)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "After editing contact:", x)
        
        
        