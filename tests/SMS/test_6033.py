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

class test_main(GaiaTestCase):
    
    _testMsg     = "This text has multiple spaces 1 2 3 4 5."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        #
        # Remove number and import contact.
        #
        self.telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Send a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.addNumberInToField(self.telNum)
        self.messages.enterSMSMsg(self._testMsg)
        self.messages.sendSMS()
        
        #
        # Check the receievd message.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x.text == self._testMsg, 
                        "The text in the message received matches the message that was sent." +\
                        "|EXPECTED: '" + self._testMsg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")
