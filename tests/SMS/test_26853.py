#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time

class test_main(GaiaTestCase):
    test_msgs = ["First message", "Second message", "Third message"]
    
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
        # Make sure we have no threads
        #
        self.messages.launch()
        self.messages.deleteAllThreads()
        
        #
        # Create and send some new tests messages. THIS ASSUMES THE TARGET
        # TELEPHONE NUMBER IS THE SAME DEVICES WHICH IS SENDING THEM.
        #

        self.messages.createAndSendSMS([self.target_telNum], self.test_msgs[0])
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()

        for i in range(2):
            self.messages.enterSMSMsg(self.test_msgs[i + 1])
            self.messages.sendSMS()
            returnedSMS = self.messages.waitForReceivedMsgInThisThread()
 
        #
        # Go into edit mode..
        #
        x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()
        
        #
        # Select Delete Messages
        #

        x = self.UTILS.getElement(DOM.Messages.delete_messages_btn, 
            "Delete messages button")
        x.tap()

        #
        # Tap Selected all
        #
        x = self.UTILS.getElement(DOM.Messages.edit_msgs_sel_all_btn, 
            "Select all button")
        x.tap()

        #
        # Tap delete
        #
        self.messages.deleteSelectedMessages()
        
        #
        # Check conversation isn't there anymore.
        #
        self.UTILS.waitForNotElements(("xpath", 
            DOM.Messages.thread_selector_xpath.format(self.target_telNum)),"Thread")
 
        time.sleep(1)
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of final position:", fnam)  
