from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Sometimes causes a problem if not cleared.
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        # Create message - 20 x 10 chars.
        sms_message = "0123456789" * 20
        sms_message_length = len(sms_message)
        self.UTILS.reporting.logComment("Message length sent: " + str(sms_message_length))

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.phone_number], sms_message)

        # Check that this last message is not marked as failed.
        time.sleep(1)
        x = self.messages.last_message_in_this_thread()
        self.UTILS.test.test("error" not in x.get_attribute("class"),
                         "The last message in this thread is not marked with error icon.")
