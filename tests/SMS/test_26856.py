from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Start a new sms.
        #
        self.messages.startNewSMS()

        #
        # Enter a number in the target field.
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Tap the message area.
        #
        message_body = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message body input field")
        message_body.tap()

        send_btn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        send_btn.tap()
        empty_warning = self.UTILS.element.getElement(DOM.Messages.empty_msg_body_warning, "Empty message warning")
        self.UTILS.test.test(empty_warning, "Warning message expected")
