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

        time.sleep(2)
           
        #
        # Create and send some new tests messages.
        #
        self.messages.createAndSendSMS([self.target_telNum], self.test_msgs[0])
        self.messages.waitForReceivedMsgInThisThread()
          
        for i in range(2):
            self.messages.enterSMSMsg(self.test_msgs[i + 1])
            self.messages.sendSMS()
            returnedSMS = self.messages.waitForReceivedMsgInThisThread()
 
        #
        # Check how many elements are there
        #
        original_count = self.messages.countMessagesInThisThread()
        self.UTILS.logResult("info",
                             "Before deletion there were " + str(original_count) +
                              " messages in this thread.")
        
        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread([1])
        
        #
        # Check message isn't there anymore.
        #
        x = self.UTILS.getElements(DOM.Messages.message_list,"Messages")
        final_count = len(x)
        real_count= original_count-1
        self.UTILS.TEST(final_count == (original_count-1), 
                        "After deleting the message, there were " + \
                        str(real_count) + \
                        " messages in this thread (" + str(final_count) + " found).")      
