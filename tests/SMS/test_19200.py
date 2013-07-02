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
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        
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
        self.messages.startNewSMS()
        
        #
        # Enter the number.
        #
        self.messages.addNumberInToField(self.target_telNum)
         
        #
        # Enter the message.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Send the SMS.
        #
        self.messages.sendSMS()
        
        #
        # Lock the phone immediately.
        #
        self.lockscreen.lock()
        
        #
        # Wait for the notification.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.lockscreen_notif_xpath % self.target_telNum), 
                                   "New message notification while screen is locked", False, 120, False)
