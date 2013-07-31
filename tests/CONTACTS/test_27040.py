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
    
    _RESTART_DEVICE = True

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
        self.contacts.importFromGmail_login(self.gmail_u, self.gmail_p)
        
        #
        # Check the Import button is disabled to begin with.
        #
        x = self.UTILS.getElement(DOM.Contacts.gmail_import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")
        
        #
        # Select / de-select contacts and make sure Import button is enabled / disabled
        # as expected.
        #
        self.UTILS.logResult("info", "Enable contact 1...")
        self.contacts.toggleSelectGmailContact(1)
        
        x = self.UTILS.getElement(DOM.Contacts.gmail_import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Enable contact 2...")
        self.contacts.toggleSelectGmailContact(2)
        
        x = self.UTILS.getElement(DOM.Contacts.gmail_import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")



        self.UTILS.logResult("info", "Disable contact 2...")
        self.contacts.toggleSelectGmailContact(2)
        
        x = self.UTILS.getElement(DOM.Contacts.gmail_import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.logResult("info", "Disable contact 1...")
        self.contacts.toggleSelectGmailContact(1)
        
        x = self.UTILS.getElement(DOM.Contacts.gmail_import_import_btn, "Import button")
        self.UTILS.TEST(x.get_attribute("disabled") == "true", "Import button is disabled.")


        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


