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

class test_6035(GaiaTestCase):
    _Description = "CLONE - Verify that If the name of the contact is empty: Phone Number as the main header."
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)
        
        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Contact_1

        #
        # Set given and family name to empty string
        #
        self.contact_1["givenName"] = ""
        self.contact_1["familyName"] = ""
        self.contact_1["name"] = "" 
        self.contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
        #
        # Import this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Clear out any current messages.
        #
        self.messages.launch()
    
        #
        # Create SMS.
        #
        self.messages.startNewSMS()
        self.messages.addNumberInToField(self.contact_1["tel"]["value"])
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Verify the number is shown in the header as there is no contact name
        #
        self.messages.checkThreadHeader(str(self.contact_1["tel"]["value"]))
