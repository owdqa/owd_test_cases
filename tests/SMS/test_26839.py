#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
#from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
        
#         #
#         # Wait for the last message in this thread to be a 'recieved' one.
#         #
#         returnedSMS = self.messages.waitForReceivedMsgInThisThread()
#         self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)
#         
#         #
#         # TEST: The returned message is as expected (caseless in case user typed it manually).
#         #
#         sms_text = returnedSMS.text
#         self.UTILS.TEST((sms_text.lower() == self._TestMsg.lower()), 
#             "SMS text = '" + self._TestMsg + "' (it was '" + sms_text + "').")

