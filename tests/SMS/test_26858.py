#===============================================================================
# 26858: Verify that the SMS message thread shows the timestamp with AM or PM
#
# Procedure:
# 1- Open SMS app
# 2- Send a sms before of 12:00
# 3- Send a sms after 12:00
# 4- Open sms conversation
#
# Expected results:
# The SMS message thread shows the timestamp with AM or PM depending on when
# the message has been sent.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.incoming_sms_num = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.date_and_time.setTimeToSpecific(p_hour=10, p_minute=0)

        self.messages.launch()
        self.send_and_check_sms("10:0", "AM")
        self.apps.kill_all()

        self.messages.launch()
        self.UTILS.date_and_time.setTimeToSpecific(p_hour=14, p_minute=0)
        self.send_and_check_sms("2:0", "PM")

    def send_and_check_sms(self, expected_time, expected_ampm):
        # Send a new sms and check the time is correct
        test_msg = "Test message at {}".format(time.time())
        self.UTILS.messages.create_incoming_sms(self.phone_number, test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
        incoming_num = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num,
                                                frame_to_change=DOM.Messages.frame_locator, timeout=5)

        tot = self.messages.timeOfThread(incoming_num)
        self.UTILS.test.test(tot.index(expected_time) != -1 and tot.index(expected_ampm) != -1,
                             "Expected: {}({}) Actual: {}".format(expected_time, expected_ampm, tot))
