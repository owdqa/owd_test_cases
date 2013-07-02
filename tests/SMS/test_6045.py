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

class test_main(GaiaTestCase):
    
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
        self.data_layer.insert_contact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now). 
        #
        self.messages.createAndSendSMS( [self.Contact_1["tel"]["value"]], "Test message.")
        self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Open contacts app and modify the contact used to send the SMS in the previous step
        #
        self.contacts.launch()
        self.Contact_2 = MockContacts().Contact_2
        self.Contact_2["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.Contact_2["tel"]["value"])
        self.contacts.editContact(self.Contact_1,self.Contact_2)
        
        #
        # Re-launch messages app.
        #
        self.messages.launch()
        
        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.logComment("Trying to open the thread with name: " + self.Contact_2["name"])
        self.messages.openThread(self.Contact_2["name"])
