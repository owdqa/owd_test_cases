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
    
        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_multiplePhones
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.viewContact(self.cont["name"])
        
        tel_counter = len(self.cont["tel"])
        for i in range(0,tel_counter):
            x = self.UTILS.getElement(("xpath", DOM.Contacts.view_contact_tels_xpath % self.cont["tel"][i]["value"]), 
                                       "Telephone number button for %s" % self.cont["tel"][i]["value"])
            self.UTILS.TEST(self.cont["tel"][i]["value"] in x.text,
                        "Phone number '%s' matches the expacted value ('%s')" % (x.text, self.cont["tel"][i]["value"]))
         
            self.UTILS.waitForElements(("id", DOM.Contacts.sms_button_specific_id % i), 
                                       "Send SMS button for %s"% self.cont["tel"][i]["value"])
         
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contact:", x)
