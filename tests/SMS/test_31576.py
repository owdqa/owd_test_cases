#===============================================================================
# 31576: Forward an SMS which is in a thread with more messages to a phone number
#
# Pre-requisites:
# There should be a thread created with several sent/received messages
#
# Procedure:
# 1. Open Messaging app
# 2. Open the thread and select a message
# 3. Long press on it (ER1)
# 4. Tap on Forward message option (ER2)
# 5. Introduce a phone number in the 'To' field
# 6. Tap on Send key (ER3)
#
# Expected results:
# ER1. Message module options menu is shown
# ER2. New message composer screen is shown with the message to be forwarded in
# the text field. The 'To' field is empty.
# ER3. The message is sent correctly
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from marionette import Actions


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

        # Send several messages to have something in the threads
        for i in range(4):
            sms_message = "Message {} " + "0123456789" * 5
            sms_message = sms_message.format(i)
            self.UTILS.messages.create_incoming_sms(self.phone_number, sms_message)
            self.UTILS.statusbar.wait_for_notification_toaster_detail(sms_message, timeout=120)

        self.messages.launch()
        self.messages.openThread(self.incoming_sms_num[0])
        self.messages.forwardMessage("sms", self.phone_number)
