#===============================================================================
# 26859: Verify the timestamp (received message) when the SMS has
# been sent from a different timezone
#
# Expected result:
# The device must show the timestamp according to the date/time configured in
# settings.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.settings import Settings
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.settings = Settings(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cp_incoming_number = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')
        self.test_msg = "Test message."
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.UTILS.date_and_time.setTimeToNow("Europe", "Madrid")
        #
        # Create and send a new test message.
        #
        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        #
        # Check the time of this message.
        #
        time.sleep(2)
        _orig_msg_timestamp = self.messages.timeOfLastMessageInThread()
        self.UTILS.reporting.debug("*** original message timestamp = '{}'".format(_orig_msg_timestamp))

        #
        # Return to the threads screen and check the time of this thread.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        time.sleep(1)

        #
        # Get the time of this thread.
        #
        _orig_thread_timestamp = self.messages.timeOfThread(title)
        self.UTILS.reporting.debug("*** original thread timestamp = '{}'".format(_orig_thread_timestamp))

        #
        # Change to a (unlikely!) timezone.
        #
        self.apps.kill_all()
        self.UTILS.date_and_time.setTimeToNow("Antarctica", "Casey")

        #
        # Open the sms app again.
        #
        self.messages.launch()

        #
        # Get the new thread time.
        #
        _new_thread_timestamp = self.messages.timeOfThread(title)
        self.UTILS.reporting.debug("*** new thread timestamp = '{}'".format(_new_thread_timestamp))

        #
        # Open our thread.
        #
        self.messages.openThread(title)

        #
        # Get the new message time.
        #
        _new_msg_timestamp = self.messages.timeOfLastMessageInThread()
        self.UTILS.reporting.debug("*** new message timestamp = '{}'".format(_new_msg_timestamp))

        self.UTILS.test.TEST(_orig_thread_timestamp != _new_thread_timestamp, "Thread timestamp has changed.")
        self.UTILS.test.TEST(_orig_msg_timestamp != _new_msg_timestamp, "Message timestamp has changed.")
