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
        self.Contact_1 = MockContact()
        self.Contact_2 = MockContact()
        
        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.insertContact(self.Contact_2)
        
        self.listNames=[self.Contact_1["givenName"],self.Contact_2["givenName"]]
        self.listSurnames=[self.Contact_1["familyName"],self.Contact_2["familyName"]]
        
        self.listNames.sort()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Verify contacts shown are the contact inserted.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list,"Contacts list")
            
        j=0
        for i in x:
            
            self.UTILS.TEST(self.listNames[j] in i.text, "The contact shown "+i.text+" has the name "+self.listNames[j])
            self.UTILS.TEST(self.listSurnames[j] in i.text, "The contact shown "+i.text+" has the surname "+self.listSurnames[j])
            j=j+1