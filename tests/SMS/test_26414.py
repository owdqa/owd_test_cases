from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Sometimes causes a problem if not cleared.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        #
        # Create message - 20 x 10 chars.
        #
        sms_message = "0123456789" * 20

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], sms_message)
        send_time = self.messages.last_sent_message_timestamp()

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        returnedSMS = self.messages.wait_for_message(send_time=send_time)
        self.UTILS.test.test(returnedSMS, "A received message appeared in the thread.", True)

        self.messages.check_last_message_contents(sms_message)
