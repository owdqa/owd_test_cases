#===============================================================================
# 31577: Forward an SMS which is in a thread with more messages to a contact
#
# Pre-requisites:
# There is at least one thread in the message app with several messages
# There is at least one contact in the contact list
#
# Procedure:
# 1. Open Messaging app
# 2. Open the thread and select a message
# 3. Long press on it (ER1)
# 4. Tap on Forward message option (ER2)
# 5. Tap on '+' icon to select a contact (ER3)
# 6. Tap on a contact (ER4)
# 7. Tap on Send key (ER5)
#
# Expected results:
# ER1. Message module options menu is shown
# ER2. New message composer screen is shown with the message to be forwarded in
# the text field. The 'To' field is empty.
# ER3. The list of contacts is shown
# ER4. The contact is added into the 'To' field
# ER5. The message is sent correctly
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

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
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("GLOBAL_CP_NUMBER").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

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
        self.messages.forwardMessageToContact("sms", self.contact["name"])
