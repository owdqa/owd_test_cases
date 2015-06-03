#
# 26997
#
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

        self.dummy_nums = ["00342222222", "+343333333"]
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Create and send a new test message containing all of our CORRECT numbers..
        msg_app = self.messages.launch()
        msg_text = "International num: {}, and {}.".format(self.dummy_nums[0], self.dummy_nums[1])
        self.UTILS.messages.create_incoming_sms(self.phone_number, msg_text)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(msg_text, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        sms = self.messages.last_message_in_this_thread()

        # Tap the number to call.
        msg_nums = sms.find_elements("tag name", "a")

        self.UTILS.test.test(len(msg_nums) == 2,
                    "There are <b>{}</b> numbers highlighted in the received text (expected <b>2</b>).".\
                    format(len(msg_nums)))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "SMS in app", x)

        self.try_number(msg_nums, 1)

        # Kill everything, then re-launch the messaging app etc ...
        self.apps.kill(msg_app)
        time.sleep(3)
        self.messages.launch()
        self.messages.openThread(title)
        x = self.messages.last_message_in_this_thread()
        msg_nums = x.find_elements("tag name", "a")
        self.try_number(msg_nums, 0)

    def try_number(self, p_msgs, p_num):
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
        self.UTILS.test.test(link_num in x_num, "Expected number ({}) matches number in dialer ({}).".\
                             format(link_num, x_num))
