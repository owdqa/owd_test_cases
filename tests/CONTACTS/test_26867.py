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
        self.cont1 = MockContacts().Contact_1
        self.cont2 = MockContacts().Contact_2
        self.cont3 = MockContacts().Contact_3
        self.cont4 = MockContacts().Contact_4
        self.cont5 = MockContacts().Contact_5
        self.cont6 = MockContacts().Contact_6
        self.cont7 = MockContacts().Contact_7
        self.cont8 = MockContacts().Contact_8
        self.cont9 = MockContacts().Contact_9
        self.cont10 = MockContacts().Contact_10
        
        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        self.data_layer.insert_contact(self.cont3)
        self.data_layer.insert_contact(self.cont4)
        self.data_layer.insert_contact(self.cont5)
        self.data_layer.insert_contact(self.cont6)
        self.data_layer.insert_contact(self.cont7)
        self.data_layer.insert_contact(self.cont8)
        self.data_layer.insert_contact(self.cont9)
        self.data_layer.insert_contact(self.cont10)
        
        self.listContacts=[self.cont1["givenName"],self.cont2["givenName"],self.cont3["givenName"],
                           self.cont4["givenName"],self.cont5["givenName"],self.cont6["givenName"],
                           self.cont7["givenName"],self.cont8["givenName"],self.cont9["givenName"],
                           self.cont10["givenName"]]
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
        
