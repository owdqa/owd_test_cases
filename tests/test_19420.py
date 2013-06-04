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

class test_19420(GaiaTestCase):
    _Description = "[BASIC][SMS] Receive a sms with vibration (device unlocked) & confirm notification - verify that the notification is fired and that you can see the message received from the other phone."
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = AppMessages(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Start by making sure we have no other notifications.
        #
        self.UTILS.clearAllStatusBarNotifs()
         
        #
        # Launch messages app.
        #
        self.messages.launch()
         
        #
        # Delete all threads.
        #
        self.messages.deleteAllThreads()
          
        #
        # Create and send a new test message (don't use api - I want to be back in homepage
        # before the sms has finshed sending and the api waits).
        #
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        newMsgBtn.tap()
        
        self.messages.addNumberInToField(self.target_telNum)        
        self.messages.enterSMSMsg(self._TestMsg)
        
        # This wasn't always quick enough so I'm trying js to make it faster ...
#         sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
#         sendBtn.tap()        
        self.marionette.execute_script("document.getElementById('" + \
                                             DOM.Messages.send_message_button[1] + \
                                             "').click();")
        
        #
        # Bit of a race: QUICKLY go 'home' and wait for the notifier.
        # If we're not quick enough the returned sms will arrive while we're still in
        # messaging, in which case the statusbar notifier will never appear.
        #
        self.UTILS.goHome()
        self.messages.waitForSMSNotifier(self.target_telNum)
        
        #
        # Click the notifier.
        #
        self.messages.clickSMSNotifier(self.target_telNum)
          
        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        sms_text = returnedSMS.text
        self.UTILS.TEST((sms_text.lower() == self._TestMsg.lower()), 
            "SMS text = '" + self._TestMsg + "' (it was '" + sms_text + "').")
         
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        #
        # Check the message via the thread.
        #
        self.messages.openThread(self.target_telNum)
        
        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        sms_text = returnedSMS.text
        self.UTILS.TEST((sms_text.lower() == self._TestMsg.lower()), 
            "SMS text = '" + self._TestMsg + "' (it was '" + sms_text + "').")

