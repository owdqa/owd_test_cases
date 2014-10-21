from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


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
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.test_msg = "Test."

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.phone_number], self.test_msg)
        send_time = self.messages.last_sent_message_timestamp()

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread(send_time=send_time)
        self.UTILS.test.TEST(returnedSMS, "A received message appeared in the thread.", True)

        self.messages.check_last_message_contents(self.test_msg)
