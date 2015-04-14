#
# 27760: Try to send an SMS when the introduced text has been deleted.
#
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from gaiatest.apps.keyboard.app import Keyboard


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.keyboard = Keyboard(self.marionette)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

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
        # Enter a message the message area.
        #
        test_msg = "test message"
        self.messages.enterSMSMsg(test_msg)

        #
        # Check the 'Send' button is now enabled.
        #
        send_btn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.test(send_btn.is_enabled(), "Send button is enabled when everything's filled in.")

        #
        # Delete the text (we should already be in the message area with the
        # keyboard present, but we need to 'manually' use the keyboard for this).
        #
        for i in range(len(test_msg)):
            self.keyboard.tap_backspace()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        msg_area = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message area")
        self.UTILS.test.test(msg_area.text == "", "Message area is clear after deleting all characters in it.")

        #
        # Check the Send button isn't enabled any more.
        #
        send_btn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.test(not send_btn.is_enabled(), 
                        "Send button is not enabled after target number is supplied, but message still empty.")

