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
from tests.mock_data.contacts import MockContacts

class test_19422(GaiaTestCase):
    _Description = "[BASIC][CONTACTS] Edit a contact changing the name and the phone number - verify that the values modified in the contact appear when viewing the updated contact."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = AppContacts(self)
                
        #
        #

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_2 = MockContacts().Contact_2

        #
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.data_layer.insert_contact(self.Contact_1)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Edit the contact with the new details.
        #
        self.contacts.editContact(self.Contact_1, self.Contact_2)
        
        #
        # TEST: The 'view contact' page shows the correct details for this new contact.
        #
        self.contacts.checkViewContactDetails(self.Contact_2)         
        
        #
        # TEST: The 'edit contact' page shows the correct details for this new contact.
        #
        self.contacts.checkEditContactDetails(self.Contact_2) 

  
        
