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

        self.gmail_u = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_p = self.UTILS.get_os_variable("GMAIL_1_PASS")

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
        self.contacts.import_GmailLogin(self.gmail_u, self.gmail_p)
        
        #
        # Check the Import button is disabled to begin with.
        #
        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Tap the Select All button (can't be done with marionette yet).
        #
        self.UTILS.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_select_all[1])
        time.sleep(1)
            
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Tapping the 'Deselect All' button ...")
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_desel_all[1])
        time.sleep(1)
            
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")


        
        #
        # Now select one contact and press Deselect all...
        #
        self.contacts.import_toggleSelectContact(1)
        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Tapping the 'Deselect All' button ...")
        self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_desel_all[1])
        time.sleep(1)
            
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)

        x = self.UTILS.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")


