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
        # Sometimes causes a problem if not cleared.
        #
        self.UTILS.clearAllStatusBarNotifs()

        #
        # Create message - 20 x 10 chars.
        #
        sms_message = ""
        for i in range(0,20):
            sms_message = sms_message + "0123456789"
            
        sms_message_length = len(sms_message)
        self.UTILS.logComment("Message length sent: " + str(sms_message_length))
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], sms_message)

        #
        # Check that this last message is not marked as failed.
        #
        time.sleep(1)
        x = self.messages.lastMessageInThisThread()
        self.UTILS.TEST( "error" not in x.get_attribute("class"),
                         "The last message in this thread is not marked with error icon.")
        
