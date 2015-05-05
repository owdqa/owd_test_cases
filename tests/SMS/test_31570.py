#
# 31570: Forward an SMS to multiple recipients
#
import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Prepare the contact we're going to insert.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.contact)
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        # Create message - 5 x 10 chars.
        timestamp = " {}".format(time.time())
        sms_message = "0123456789" * 5 + timestamp
        self.UTILS.reporting.logComment("Message length sent: {}".format((len(sms_message))))

        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_message)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(timestamp, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        self.messages.forwardMessageToMultipleRecipients("sms", self.phone_number, self.contact["name"])
