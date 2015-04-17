#
# 27742
#
from OWDTestToolkit import DOM
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(PixiTestCase):

    test_msg = "This text has multiple spaces 1  2  3  4  5."

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Remove number and import contact.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        #
        # Check the receievd message.
        #
        self.messages.check_last_message_contents(self.test_msg)
