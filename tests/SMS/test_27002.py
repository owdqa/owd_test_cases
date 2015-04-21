#
# 27002: Verify that when tapping in a SMS with several valid phone numbers,
# the dialer is launched with the phone number tapped on pre-filled in.
#
import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.dialer import Dialer


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        # Create and send a new test message containing all of our numbers..
        nums = ["12345678", "123456789", "01234567", "012345678"]
        sms_msg = "Test numbers {}".format(", ".join(nums))
        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(sms_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        sms = self.messages.last_message_in_this_thread()

        #
        # Tap the numbers to call.
        #
        msg_nums = sms.find_elements(*DOM.Messages.phone_info_in_msg)

        for i in range(len(msg_nums)):
            num = msg_nums[i]
            self.UTILS.reporting.info("************ TAPPING NUMBER {}: {}".format(i, num.text))
            num.tap()
            num_text = num.text

            call_btn = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "Call button")
            call_btn.tap()

            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

            #
            # Dialer is started with the number already filled in.
            #
            time.sleep(1)
            phone_number = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number")
            self.UTILS.test.test(num_text == phone_number.get_attribute("value"),
                            "The dialer number contains '{}' (expected '{}').".\
                            format(num_text, phone_number.get_attribute("value")))

            time.sleep(3)
            #
            # Switch back to messaging app (without killing anything) etc ...
            #
            running_apps = [app.origin for app in self.apps.running_apps(True)]
            self.messages.launch()
            self.UTILS.reporting.info("********* RUNNING APPS: {}".format(running_apps))
            if not 'app://sms.gaiamobile.org' in running_apps:
                self.UTILS.reporting.info("****************** SMS Not running, opening thread")
                self.messages.openThread(title)
            else:
                self.UTILS.reporting.info("****************** SMS RUNNING")

            # We need to recover the last message and the numbers, since the reference is lost in
            # the frame changes
            sms = self.messages.last_message_in_this_thread()
            msg_nums = sms.find_elements(*DOM.Messages.phone_info_in_msg)
