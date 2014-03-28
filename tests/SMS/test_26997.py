#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.dummy_nums = ["2222222", "3333333"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Create and send a new test message containing all of our CORRECT numbers..
        #
        msgApp = self.messages.launch()
        self.messages.createAndSendSMS([self.num1], "International num: 0034{}, and +34{}.".\
                                       format(self.dummy_nums[0], self.dummy_nums[1]))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the number to call.
        #
        msg_nums = x.find_elements("tag name", "a")

        self.UTILS.test.TEST(len(msg_nums) == 2,
                    "There are <b>2</b> numbers highlighted in the received text (there were <b>{}</b>).".\
                    format(len(msg_nums)))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "SMS in app", x)

        self._doTest(msg_nums, 1)

        #
        # Kill everything, then re-launch the messaging app etc ...
        #
        self.apps.kill(msgApp)
        time.sleep(3)
        self.messages.launch()
        self.messages.openThread(self.num1)
        x = self.messages.waitForReceivedMsgInThisThread()
        msg_nums = x.find_elements("tag name", "a")
        self._doTest(msg_nums, 0)

    def _doTest(self, p_msgs, p_num):
        link_num = self.dummy_nums[p_num]
        self.UTILS.reporting.logResult("info", "Tapping link to number: {}.".format(link_num))
        self.UTILS.reporting.logResult("info", "Link text is '{}'.".format(p_msgs[p_num].text))
        p_msgs[p_num].tap()
        time.sleep(1)

        x = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "Call button")
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        time.sleep(2)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of dialer after clicking the link for number {}".\
                                       format(link_num), x)
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number")
        x_num = x.get_attribute("value")
        self.UTILS.test.TEST(link_num in x_num, "Expected number ({}) matches number in dialer ({}).".\
                             format(link_num, x_num))
