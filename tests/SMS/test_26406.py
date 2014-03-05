#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact
#import time


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
        self.Contact_1 = MockContact()
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.messages.launch()
        
        #
        # Start a new SMS and add the message and contact name.
        #
        self.messages.startNewSMS()
    
        self.messages.selectAddContactButton()
        self.contacts.viewContact(self.Contact_1["familyName"], False)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.Contact_1["name"], True)
        
        #
        # Remove it.
        #
        self.messages.removeContactFromToField(self.Contact_1["name"])
        
        #
        # Verify the contact name is present before removing it.
        #
        self.messages.checkIsInToField(self.Contact_1["name"], False)