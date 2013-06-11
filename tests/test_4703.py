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

class test_4703(GaiaTestCase):
    _Description = "[SMS] Receive an SMS with a phone number and call to it."
    
    _TestNum = "0781234567890"
    _TestMsg = "Test number " + _TestNum + " for dialling."
        
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.phone      = Phone(self)
        
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
        # Make sure it's empty first.
        #
        self.messages.deleteAllThreads()
          
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
        
        #
        # Wait for the last message in this thread to be a 'recieved' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        x.find_element("tag name", "a").click()        
        
        time.sleep(5)
        
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Phone.frame_locator_from_sms)
        
        #
        # Dial the number.
        #
        self.phone.callThisNumber()
        
        #
        # Wait 2 seconds, then hangup.
        #
        time.sleep(2)
        self.phone.hangUp()
