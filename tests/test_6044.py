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

class test_6044(GaiaTestCase):
    _Description = "CLONE - Add a contact and verify that the SMS list now shows the name"
    
    _TestMsg     = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Import contact (adjust to the correct number).
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumberInToField(self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Open contacts app and create a contact with the same phone number used to send the SMS in the 
        # previous step
        #
        self.contacts.launch()
        self.contacts.createNewContact(self.Contact_1)
        
        #
        # Re-launch messages app.
        #
        self.messages.launch()
        
        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.logComment("Trying to open the thread with name: " + self.Contact_1["name"])
        self.messages.openThread(self.Contact_1["name"])
