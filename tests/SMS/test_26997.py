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

        self.dummy_nums = ["09876543", "12345678"]
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Create and send a new test message containing all of our CORRECT numbers..
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.num1], "International num: 0034%s, and +34 %s." %\
                                                    (self.dummy_nums[0], self.dummy_nums[1]))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the number to call.
        #
        msg_nums = x.find_elements("tag name", "a")
        
        self.UTILS.TEST(len(msg_nums) == 2,
                        "There are <b>2</b> numbers highlighted in the received text (there were <b>%s</b>)." % \
                        len(msg_nums))
        
        #
        # NOTE: Change "+34" to "0034".
        #
        self._doTest(msg_nums, 0)

        #
        # Kill everything, then re-launch the messaging app etc ...
        #
        self.apps.kill_all()
        self.messages.launch()
        self.messages.openThread(self.num1)
        x = self.messages.waitForReceivedMsgInThisThread()
        msg_nums = x.find_elements("tag name", "a")
        self._doTest(msg_nums, 1)
        
        
    def _doTest(self, p_msgs, p_num):
        link_num = self.dummy_nums[p_num]
        self.UTILS.logResult("info", "Tapping link to number: %s." % link_num)
        p_msgs[p_num].tap()
        time.sleep(1)
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
        time.sleep(2)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of dialer after clicking the link for number %s" % link_num, x)
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number")
        x_num = x.get_attribute("value")
        self.UTILS.TEST(link_num in x_num, "Expected number (%s) matches number in dialer (%s)." % (link_num, x_num))
