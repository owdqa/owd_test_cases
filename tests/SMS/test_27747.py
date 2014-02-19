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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
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
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(givenName = '', familyName = '', name = '', tel = {'type': '', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)

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
        self.messages.addNumbersInToField([ self.Contact_1["tel"]["value"] ])
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
        self.messages.checkThreadHeader(str(self.Contact_1["tel"]["value"]))
