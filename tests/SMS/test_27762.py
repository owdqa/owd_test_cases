#
# 27762: Receive an SMS with a phone number and call to it
#
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    test_num = "0781234567890"
    test_msg = "Test number " + test_num + " for dialing."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("GLOBAL_CP_NUMBER").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)

        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        last_msg = self.messages.last_message_in_this_thread()
        last_msg.find_element("tag name", "a").tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "Call button")
        x.tap()

        time.sleep(5)

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        #
        # Dial the number.
        #
        self.Dialer.callThisNumber()

        #
        # Wait 2 seconds, then hangup.
        #
        time.sleep(2)
        self.Dialer.hangUp()
        self.data_layer.kill_active_call()
