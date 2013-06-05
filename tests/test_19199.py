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

class test_19199(GaiaTestCase):
    _Description = "[SMS] (BLOCKED BY BUG 879816) Delete a SMS in a conversation with several sms."
    
    _TestMsg1 = "First message."
    _TestMsg2 = "Second message"
    _TestMsg3 = "Third message"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = AppMessages(self)
        
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
        
        
    def tearDown(self):
#         self.messages.waitForSMSNotifier("222000",5)
#         self.UTILS.clearAllStatusBarNotifs()

        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.UTILS.TEST(self.data_layer.delete_all_sms(), "Delete all SMS's.")
        time.sleep(2)

        #
        # Launch messages app.
        #
        self.messages.launch()
           
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
        # Check how many elements are there
        #
        original_count = self.messages.countMessagesInThisThread()
        self.UTILS.logResult("info",
                             "Before deletion there were " + str(original_count) + " messages in this thread.")
        
        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread([1])
        
        #
        # Check message isn't there anymore.
        #
        x = self.UTILS.getElements(DOM.Messages.thread_messages,"Messages")
        final_count = len(x)
        real_count= original_count-1
        self.UTILS.TEST(final_count == (original_count-1), 
                        "After deleting the message, there were " + \
                        str(real_count) + \
                        " messages in this thread (" + str(final_count) + " found).")      
