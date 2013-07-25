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
        self.Dialer      = Dialer(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Create and send a new test message containing all of our CORRECT numbers..
        #
        self.UTILS.logResult("info", "<b>Check CORRECT numbers are ok ...</b>")
        nums = ["12345678", "123456789"]        
        self._testAll(nums, len(nums))

        self.UTILS.logResult("info", "<b>Check INCORRECT numbers are ok ...</b>")
        nums = ["123", "1234"]        
        self._testAll(nums, 0)

    def _testAll(self, nums, tappable_count):
        sms_nums = ""
        
        for i in range(0,len(nums)):
            sms_nums = "%s, test%s %s" % (sms_nums, str(i), nums[i])
            
        sms_msg = "Test numbers: %s." % sms_nums
        
        self.apps.kill_all()
        time.sleep(2)
        self.messages.launch()
        self.messages.createAndSendSMS([self.num1], sms_msg)
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the number to call.
        #
        msg_nums = x.find_elements("tag name", "a")
        
        self.UTILS.TEST(len(msg_nums) == tappable_count,
                        "There are <b>%s</b> numbers highlighted in the received text (there were <b>%s</b>)." % \
                        (tappable_count, len(msg_nums)))
        
        for i in range(0,len(msg_nums)):
            msg_nums[i].tap()
            
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
            
            #
            # Dialler is started with the number already filled in.
            #
            x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number")
            self.UTILS.TEST(nums[i] in x.get_attribute("value"), 
                            "The phone number contains '%s' (it was '%s')." % (nums[i], x.get_attribute("value")))
            
            #
            # Kill everything, then re-launch the messaging app etc ...
            #
            self.apps.kill_all()
            time.sleep(2)
            self.messages.launch()
            self.messages.openThread(self.num1)
            x = self.messages.waitForReceivedMsgInThisThread()
            msg_nums = x.find_elements("tag name", "a")

