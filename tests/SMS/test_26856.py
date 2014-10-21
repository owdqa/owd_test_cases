from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

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
        x = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message body input field")
        x.tap()

        #
        # Check the 'Send button isn't enabled yet.
        #
        x = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.TEST(not x.is_enabled(), 
                        "Send button is not enabled after target number is supplied, but message still empty.")
