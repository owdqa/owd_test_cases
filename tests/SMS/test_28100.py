2: 

Pre-requisites:


Procedure:


Expected results:

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.incoming_sms_num = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')
        self.UTILS.reporting.logComment("Sending messages to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and send a new test message containing all of our CORRECT numbers..
        #
        self.UTILS.reporting.logResult("info", "<b>Check CORRECT numbers are ok ...</b>")
        nums = ["12345678", "123456789"]
        self.check_numbers(nums, range(2))

        self.UTILS.reporting.logResult("info", "<b>Check INCORRECT numbers are ok ...</b>")
        nums = ["123", "1234"]
        self.check_numbers(nums, [])

        self.UTILS.reporting.logResult("info", "<b>Check MIXED numbers are ok ...</b>")
        nums = ["123", "12345678", "1234"]
        self.check_numbers(nums, [1])

    def check_numbers(self, nums, tappables):
        #
        # Generate a string of the type: "Test0 <number> Test1 <number>...."
        #
        fill_text = ["Test{}".format(i) for i in range(len(nums))]
        sms_msg = "Test numbers: {}".format(" ".join([item for sublist in map(None, fill_text, nums)
                                                      for item in sublist]))

        #
        # Start each test run from scratch.
        #
        self.apps.kill_all()
        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(sms_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()

        #
        # Get the numbers in the SMS
        #
        msg_nums = sms.find_elements("tag name", "a")

        description = "There are <b>{}</b> numbers highlighted in the received text (expected <b>{}</b>)."
        self.UTILS.test.TEST(len(msg_nums) == len(tappables), description.format(len(msg_nums), len(tappables)))
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
            time.sleep(1)
            number = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number").get_attribute("value")
            description = "The phone number is '{}' (expected '{}').".format(number, nums[tappables[i]])
            self.UTILS.test.TEST(nums[tappables[i]] == number, description)

            #
            # Kill everything, then re-launch the messaging app etc ...
            #
            self.messages.launch()

            sms = self.messages.lastMessageInThisThread()
            msg_nums = sms.find_elements("tag name", "a")
