#
# 26851: Receive a sms while device is locked(Vibration alert), screen off
#
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(SpreadtrumTestCase):

    test_msg = "Test message."

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)

        # Lock the phone immediately.
        self.data_layer.set_setting("lockscreen.enabled", True)

        # Wait for the notification.
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
