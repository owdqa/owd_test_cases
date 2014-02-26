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
    NUM_CONTACTS = 10;
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
        self.mock_contacts = [MockContact() for i in range(self.NUM_CONTACTS)]

        map(self.UTILS.insertContact, self.mock_contacts)
        
        self.listContacts = [c["givenName"] for c in self.mock_contacts]
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Verify list has 'NUM_CONTACTS' contacts.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list,"Contacts list")
        self.counterContacts = len(x)
        self.UTILS.TEST(self.NUM_CONTACTS == self.counterContacts, "All contacts are showed")
        
        #
        # Verify contacts shown are the contact inserted.
        #
        count = 0
        areThere = False;
        for i in x:
            for c in self.listContacts:
                if (c in i.text):
                    self.UTILS.logResult("info", "Contact " + c + " inserted");
                    count += 1;
                    break;

        self.UTILS.TEST(count == self.NUM_CONTACTS, "All contacts inserted")