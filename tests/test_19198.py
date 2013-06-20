#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_19198(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 879816) [SMS] Delete all SMS in a conversation with several sms."    
    _TestMsg1 = "First message."
    _TestMsg2 = "Second message"
    _TestMsg3 = "Third message"
    
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app & delete all Threads
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
        self.messages.launch()
#         self.messages.deleteAllThreads()
        
        #
        # Create and send some new tests messages.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg1)
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.messages.enterSMSMsg(self._TestMsg2)
        self.messages.sendSMS()
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.messages.enterSMSMsg(self._TestMsg3)
        self.messages.sendSMS()
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
 
        #
        # Go into edit mode..
        #
        x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()
        
        #
        # Tap Selected all
        #
        x = self.UTILS.getElement(DOM.Messages.edit_msgs_sel_all_btn, "Select all button")
        x.tap()

        #
        # Tap delete
        #
        self.messages.deleteSelectedMessages()
        
        #
        # Check conversation isn't there anymore.
        #
        self.UTILS.waitForNotElements(("xpath", DOM.Messages.thread_selector_xpath % self.target_telNum),"Thread")
 
        time.sleep(1)
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of final position:", fnam)  
