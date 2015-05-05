from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time

class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Start with no SMS.
        self.data_layer.delete_all_sms()

        # Get the correct number for the sms device.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()
        """
        Send a message to an invalid number to create a thread with just an
        outgoing message..
        """

        msg_text = str(time.time())
        self.messages.create_and_send_sms([self.phone_number], msg_text)
        self.messages.wait_for_message()

        # Return to the threads view.
        self.messages.go_back()

        # Get the preview txt for our test.
        preview_text = self.messages.getThreadText(self.phone_number)

        self.UTILS.test.test(preview_text in msg_text,
                        "Preview text ({}) is in the original message text({}).".format(preview_text, msg_text))
