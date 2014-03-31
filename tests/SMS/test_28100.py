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
import time


class test_main(GaiaTestCase):

    test_msg = "Test message."
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Create and send a new test message containing all of our CORRECT numbers..
        #
        self.UTILS.reporting.logResult("info", "<b>Check CORRECT numbers are ok ...</b>")
        nums = ["12345678", "123456789"]
        self._testAll(nums, len(nums))

        self.UTILS.reporting.logResult("info", "<b>Check INCORRECT numbers are ok ...</b>")
        nums = ["123", "1234"]
        self._testAll(nums, 0)

        self.UTILS.reporting.logResult("info", "<b>Check MIXED numbers are ok ...</b>")
        nums = ["123", "12345678", "1234"]
        self._testAll(nums, 1)

    def _testAll(self, nums, tappable_count):
        #
        # Generate a string of the type: "Test0 <number> Test1 <number>...."
        #
        fill_text = ["Test{}".format(i) for i in range(len(nums))]
        sms_msg = "Test numbers: {}".format(" ".join([item for sublist in map(None, fill_text, nums)
                                                      for item in sublist]))

        #
        # Start from clean for each test run.
        #
        self.apps.kill_all()
        time.sleep(2)
        self.messages.launch()
        self.messages.createAndSendSMS([self.num1], sms_msg)
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the number to call.
        #
        msg_nums = x.find_elements("tag name", "a")

        description = "There are <b>{}</b> numbers highlighted in the received text (there were <b>{}</b>)."
        self.UTILS.test.TEST(len(msg_nums) == tappable_count, description.format(tappable_count, len(msg_nums)))

        for i in range(len(msg_nums)):
            msg_nums[i].tap()

            #
            # Press Call button from options overlay
            #
            x = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "Call button")
            x.tap()

            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

            #
            # Dialer is started with the number already filled in.
            #
            description = "The phone number contains '{}' (it was '{}')."
            x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number")
            self.UTILS.test.TEST(nums[i] in x.get_attribute("value"),
                            description.format(nums[i], x.get_attribute("value")))

            #
            # Kill everything, then re-launch the messaging app etc ...
            #
            self.messages.launch()

            #
            # This may seem repetitive, but it looks like the reference to the
            # a HTML elements is lost when switching from apps
            #
            x = self.messages.waitForReceivedMsgInThisThread()
            msg_nums = x.find_elements("tag name", "a")
