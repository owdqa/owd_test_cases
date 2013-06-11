#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.mock_data.contacts import MockContacts

class test_19423(GaiaTestCase):
    _Description = "[BASIC][CONTACTS] Add new contact filling all the fields - verify the contact is added with the correct values for each field."
 
    def setUp(self):
            
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        
        #
        # Get details of our test contact.
        #
        self.Contact_1 = MockContacts().Contact_1
        
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Store our picture on the device.
        #
        self.UTILS.addFileToDevice('./tests/resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Create our contact.
        #
        self.contacts.createNewContact(self.Contact_1,"gallery")
        
        #
        # Verify our contact.
        #
        self.contacts.verifyImageInAllContacts(self.Contact_1['name'])
        self.contacts.checkViewContactDetails(self.Contact_1, True)
