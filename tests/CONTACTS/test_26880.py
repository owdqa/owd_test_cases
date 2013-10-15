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
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
 
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
        self.cont = MockContacts().Contact_1
        
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
    
        #
        # Store our picture on the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Create our contact.
        #
        self.contacts.createNewContact(self.cont,"gallery")
        
        #
        # Verify our contact.
        #
        self.contacts.verifyImageInAllContacts(self.cont['name'])

        self.UTILS.waitForElements(DOM.Contacts.view_all_contact_JSname, "Name John Smith")