#===============================================================================
# 31574: Cancel forwarding a message
#
# Procedure:
# 1. Open Messaging app
# 2. Open the message
# 3. Long press on it (ER1)
# 4. Tap on 'Cancel' option
#
# Expected results:
# ER1. Message module options menu is shown
# ER2. User is taken back to the message from where the message module options
# menu was launched
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from marionette import Actions
import time


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.actions = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        timestamp = " {}".format(time.time())
        sms_message = "0123456789" * 5 + timestamp
        self.UTILS.reporting.logComment("Message length sent: {}".format((len(sms_message))))

        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_message)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(timestamp, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        #
        # Open sms option with longtap on it
        #
        self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
        sms = self.messages.last_message_in_this_thread()
        body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
        self.actions.long_press(body, 2).perform()

        #
        # Press cancel button
        #
        self.UTILS.reporting.logResult("info", "Clicking cancel button")
        time.sleep(2)
        cancel_btn = self.UTILS.element.getElement(DOM.Messages.cancel_btn_msg_opt, "Cancel button is displayed")
        self.UTILS.reporting.debug("*** Cancel button: {}   text: {}".format(cancel_btn, cancel_btn.text))
        self.UTILS.element.simulateClick(cancel_btn)
