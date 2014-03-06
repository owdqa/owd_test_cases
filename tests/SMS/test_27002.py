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
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps import Dialer

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.dialer     = Dialer(self)

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
        nums = ["12345678", "123456789", "01234567", "012345678"]
        sms_nums = ""
        for i in nums:
            sms_nums = "{}, {}".format(sms_nums, i)
        sms_msg = "Test numbers {}.".format(sms_nums)
         
        self.messages.createAndSendSMS([self.num1], sms_msg)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the numbers to call.
        #
        msg_nums = x.find_elements("tag name", "a")
        
        for i in range(0,len(msg_nums)):
            msg_nums[i].tap()

            x = self.UTILS.getElement(DOM.Messages.header_call_btn, "Call button")
            x.tap()
            
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
            
            #
            # Dialler is started with the number already filled in.
            #
            x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number")
            self.UTILS.TEST(nums[i] in x.get_attribute("value"), 
                            "The dialer number contains '%s' (it was '%s')." % (nums[i], x.get_attribute("value")))
            
            #
            # Switch back to messaging app (without killing anything) etc ...
            #
            self.messages.launch()
                        
            #
            # This may seem repetitive, but it looks like the referece to the 
            # a HTML elements is lost when switching from apps
            #    
            x = self.messages.waitForReceivedMsgInThisThread()
            msg_nums = x.find_elements("tag name", "a")

