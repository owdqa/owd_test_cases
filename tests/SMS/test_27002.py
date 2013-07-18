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
        self.phone      = Phone(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message containing all of our numbers..
        #
        nums = ["123456678", "123456789", "01234567", "012345678"]
        sms_nums = ""
        for i in nums:
            sms_nums = "%s, %s" % (sms_nums, i)
        sms_msg = "Test numbers %s." % sms_nums
        
        self.messages.createAndSendSMS([self.num1], sms_msg)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the number to call.
        #
        msg_nums = x.find_elements("tag name", "a")
        
        for i in range(0,len(msg_nums)):
            msg_nums[i].tap()
            
            self.UTILS.switchToFrame(*DOM.Phone.frame_locator)
            
            #
            # Dialler is started with the number already filled in.
            #
            x = self.UTILS.getElement(DOM.Phone.phone_number, "Phone number")
            self.UTILS.TEST(nums[i] in x.get_attribute("value"), 
                            "The phone number contains '%s' (it was '%s')." % (nums[i], x.get_attribute("value")))
            
            #
            # Kill everything, then re-launch the messaging app etc ...
            #
            self.apps.kill_all()
            self.messages.launch()
            self.messages.openThread(self.num1)
            x = self.messages.waitForReceivedMsgInThisThread()
            msg_nums = x.find_elements("tag name", "a")

