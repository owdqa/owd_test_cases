#===============================================================================
# 31573: Forward a received message (only one message in the thread)
# Procedure:
# 1. Open Messaging app
# 2. Open the received message
# 3. Long press on it (ER1)
# 4. Tap on Forward message option (ER2)
# 5. Introduce a phone number in the 'To' field
# 6. Tap on Send key (ER3)
#
# Expected Results:
# ER1. Message module options menu is shown
# ER2. New message composer screen is shown with the message to be forwarded
# in the text field. The 'To' field is empty.
# ER3. The message is sent correctly
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from marionette import Actions
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.actions = Actions(self.marionette)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        # Create message
        timestamp = " {}".format(time.time())
        sms_message = "0123456789" * 5 + timestamp
        self.UTILS.reporting.logComment("Message length sent: {}".format((len(sms_message))))

        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_message)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(timestamp, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        self.messages.forwardMessage("sms", self.phone_number)
