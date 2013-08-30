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
        
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list", True, 20)
        
        gmail_contacts = []
        for y in x:
            gmail_contacts.append( y.get_attribute("data-search") )
            
        self.contacts.import_ImportAll()
        
        #
        # Check all our contacts are in the list.
        #
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_all_contact_name_xpath % self.cont["familyName"]),
                                   "Contact '%s'" % self.cont["familyName"])
        
        # ... and the gmail contacts ...
        for i in gmail_contacts:
            self.UTILS.waitForElements( ("xpath", DOM.Contacts.view_all_contact_name_xpath % i),
                                       "Contact '%s'" % i)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


