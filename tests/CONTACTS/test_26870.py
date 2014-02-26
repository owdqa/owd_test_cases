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
        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[2]["familyName"] = "Tnameir";
        self.midWord="name"
        
        map(self.UTILS.insertContact, self.test_contacts)   
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for the sought contact.
        #
        self.contacts.search(self.midWord)
        
        #
        # Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.test_contacts[2]["givenName"])
        
        #
        # Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.test_contacts[1]["givenName"],False)
        self.contacts.checkSearchResults(self.test_contacts[0]["givenName"],False)