#
# Imports which are standard for all test cases.
#
import sys
import time
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cp_incoming_number = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Start by making sure we have no other notifications.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        send_time = time.time()
        self.UTILS.messages.create_incoming_sms(self.target_telNum, self.test_msg)

        self.UTILS.statusbar.wait_for_notification_toaster_title(self.cp_incoming_number, timeout=120)

        #
        # Click the notifier.
        #
        self.UTILS.statusbar.click_on_notification_title(self.cp_incoming_number, DOM.Messages.frame_locator)

        #
        # Check received message contents
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread(send_time=send_time)
        sms_text = returnedSMS.text
        self.UTILS.test.TEST(sms_text == self.test_msg, "SMS text = '{}' (it was '{}').".\
                             format(self.test_msg, sms_text))

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Check the message via the thread.
        #
        self.messages.openThread(self.cp_incoming_number)

        #
        # Check received message contents
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread(send_time=send_time)
        sms_text = returnedSMS.text
        self.UTILS.test.TEST(sms_text == self.test_msg, "SMS text = '{}' (it was '{}').".\
                             format(self.test_msg, sms_text))
