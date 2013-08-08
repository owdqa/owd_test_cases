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
    
    _TestMsg     = "Test message."
    
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
        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.msg = "Test " + str(time.time())

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        
        self.UTILS.logResult("info", "** TEST: receive msg while in the thread.")
        self.messages.createAndSendSMS([self.num], "Test message")
        self.messages.waitForReceivedMsgInThisThread()
        
        
        # Do this 'long hand' so we can switch back to the main screen before the message finishes
        # sending (or we might miss the return notification).
        self.UTILS.logResult("info", "** TEST: receive msg while in main screen (looking at threads).")
        self.messages.enterSMSMsg(self.msg)
        x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send message button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        self.messages.waitForNewSMSPopup_by_msg(self.msg)