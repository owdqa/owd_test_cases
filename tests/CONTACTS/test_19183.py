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
        self.settings   = Settings(self)

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_2 = MockContacts().Contact_2
        self.data_layer.insert_contact(self.Contact_1)
        self.data_layer.insert_contact(self.Contact_2)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        # Jumping out here while I try to figure out how to
        # put > 1 phone number in via the mock object!
        self.UTILS.logResult("info", "Quitting test early!")
        return

        #
        # Tap the 2nd number to dial it.
        #
        
        #
        # Switch to the dialer iframe.
        #
        self.marionette.switch_to_frame()
        #self.UTILS.switchToFrame(DOM.Dialer.frame_locator, "Dialer iframe")
        
        #
        # Verify things....
