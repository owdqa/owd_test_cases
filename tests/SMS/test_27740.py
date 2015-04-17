from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

        # Start with no SMS.
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to an invalid number to create a thread with just an
        # outgoing message..
        #
        msg_text = str(time.time())
        self.messages.create_and_send_sms([self.phone_number], msg_text)

        #
        # Return to the threads view.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Get the preview txt for our test.
        #
        preview_text = self.messages.getThreadText(self.phone_number)

        self.UTILS.test.test(preview_text in msg_text,
                        "Preview text ({}) is in the original message text({}).".format(preview_text, msg_text))
