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

class test_19200(GaiaTestCase):
    _Description = "[SMS] Receive a sms while device is locked(Vibration alert), screen off."
    
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
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        newMsgBtn.tap()
        
        #
        # Enter the number.
        #
        numInput = self.UTILS.getElement(DOM.Messages.target_number, "Target number field")
        numInput.send_keys(self.target_telNum)
         
        #
        # Enter the message.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Send the SMS.
        #
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()
        
        #
        # Lock the phone immediately.
        #
        self.lockscreen.lock()
        
        #
        # Wait for the notification.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.lockscreen_notif_xpath % self.target_telNum), 
                                   "New message notification while screen is locked", False, 120, False)
