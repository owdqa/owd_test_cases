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

        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        _contacts_before = len(x)
        
        x = self.contacts.import_HotmailLogin(self.hotmail_u, self.hotmail_p)
        if not x or x == "ALLIMPORTED":
            self.UTILS.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        self.contacts.import_toggleSelectContact(1)
        
        # El.tap() not working on this just now.
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_close_icon[1])

        time.sleep(1)
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        x = self.UTILS.getElement(DOM.Contacts.settings_done, "Settings done button")
        x.tap()
        
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        _contacts_after = len(x)
        
        self.UTILS.TEST(_contacts_after == _contacts_before, "No more contacts werer imported (%s vs %s)." % \
                        (_contacts_after, _contacts_before))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "x", x)
        
        
        