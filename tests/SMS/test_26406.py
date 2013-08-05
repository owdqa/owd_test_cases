#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

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
        self.messages   = Messages(self)
        
        #
        # Import contact (adjust the correct number).
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.messages.launch()
        
        #
        # Start a new SMS and add the message and contact name.
        #
        self.messages.startNewSMS()
    
        self.messages.selectAddContactButton()
        self.contacts.viewContact(self.cont["familyName"], False)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.cont["name"], True)
        
        #
        # Remove it.
        #
        self.messages.removeContactFromToField(self.cont["name"])
        
        #
        # Verify the contact name is present before removing it.
        #
        self.messages.checkIsInToField(self.cont["name"], False)
        
        
