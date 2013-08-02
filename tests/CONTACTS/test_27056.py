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
        self.contacts.importFromHotmail_login(self.hotmail_u, self.hotmail_p)
        
        x = self.UTILS.getElements(DOM.Contacts.hotmail_import_conts_list, "Contact list")
        
        hotmail_contacts = []
        for y in x:
            hotmail_contacts.append( y.get_attribute("data-search") )
            
        self.contacts.importFromGmail_importAll()
        
        #
        # Check all our contacts are in the list.
        #
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_all_contact_name_xpath % self.cont["familyName"]),
                                   "Contact '%s'" % self.cont["familyName"])
        
        # ... and the hotmail contacts ...
        for i in hotmail_contacts:
            self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_all_contact_name_xpath % i),
                                       "Contact '%s'" % i)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


