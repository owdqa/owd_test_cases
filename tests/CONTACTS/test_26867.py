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
        self.Contact_3 = MockContact()
        self.Contact_4 = MockContact()
        self.Contact_5 = MockContact()
        self.Contact_6 = MockContact()
        self.Contact_7 = MockContact()
        self.Contact_8 = MockContact()
        self.Contact_9 = MockContact()
        self.Contact_10 = MockContact()
        
        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.insertContact(self.Contact_2)
        self.UTILS.insertContact(self.Contact_3)
        self.UTILS.insertContact(self.Contact_4)
        self.UTILS.insertContact(self.Contact_5)
        self.UTILS.insertContact(self.Contact_6)
        self.UTILS.insertContact(self.Contact_7)
        self.UTILS.insertContact(self.Contact_8)
        self.UTILS.insertContact(self.Contact_9)
        self.UTILS.insertContact(self.Contact_10)
        
        self.listContacts=[self.Contact_1["givenName"],self.Contact_2["givenName"],self.Contact_3["givenName"],
                           self.Contact_4["givenName"],self.Contact_5["givenName"],self.Contact_6["givenName"],
                           self.Contact_7["givenName"],self.Contact_8["givenName"],self.Contact_9["givenName"],
                           self.Contact_10["givenName"]]
        self.listContacts.sort()
        
        self.numContacts=10
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Verify list has 10 contacts.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list,"Contacts list")
        self.counterContacts=len(x)
        self.UTILS.TEST(self.numContacts == self.counterContacts, "All contacts are showed")
        
        #
        # Verify contacts shown are the contact inserted.
        #
        j=0
        for i in x:
            
            self.UTILS.TEST(self.listContacts[j] in i.text, "The contacts shown"+i.text+" are the same that contacts inserted"+self.listContacts[j])
            j=j+1