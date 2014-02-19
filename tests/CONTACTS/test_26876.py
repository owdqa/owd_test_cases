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
    
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel = [{'type': 'Mobile', 'value': '555555555'},
                                            {'type': 'Mobile', 'value': '666666666'}])
        self.UTILS.insertContact(self.Contact_1)
        
        
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
        self.contacts.viewContact(self.Contact_1["name"])
        
        tel_counter = len(self.Contact_1["tel"])
        for i in range(0,tel_counter):
            x = self.UTILS.getElement(("xpath", DOM.Contacts.view_contact_tels_xpath % self.Contact_1["tel"][i]["value"]),
                                       "Telephone number button for %s" % self.Contact_1["tel"][i]["value"])
            self.UTILS.TEST(self.Contact_1["tel"][i]["value"] in x.text,
                        "Phone number '%s' matches the expacted value ('%s')" % (x.text, self.Contact_1["tel"][i]["value"]))
         
            self.UTILS.waitForElements(("id", DOM.Contacts.sms_button_specific_id % i), 
                                       "Send SMS button for %s"% self.Contact_1["tel"][i]["value"])
         
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contact:", x)
