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
    
    _TestNum = "123456789"
    _TestMsg = "Test number " + _TestNum + " for dialling."
        
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.Dialer      = Dialer(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
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
        
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        a=x.find_element("tag name", "a")

        a.tap()

        x = self.UTILS.getElement(DOM.Messages.header_call_btn, "Call button")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
        
        #
        # Dial the number.
        #
        self.Dialer.callThisNumber()
        
        #
        # Wait 2 seconds, then hangup.
        #
        time.sleep(2)
        self.Dialer.hangUp()
        self.data_layer.kill_active_call()
