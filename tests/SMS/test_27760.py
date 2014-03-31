#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
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
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

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
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Enter a message the message area.
        #
        x = self.messages.enterSMSMsg("xxx")

        #
        # Check the 'Send' button is now enabled.
        #
        x = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.TEST(x.is_enabled(), 
                        "Send button is enabled when everything's filled in.")

        #
        # Delete the text (we should already be in the message area with the
        # keyboard present, but we need to 'manually' use the keyboard for this).
        #
        orig_frame = self.UTILS.iframe.currentIframe()

        for i in range(3):
            self.keyboard.tap_backspace()
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame("src", orig_frame)

        x = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message area")
        self.UTILS.test.TEST(x.text == "", "Message area is clear after deleting all characters in it.")

        #
        # Check the 'Send button isn't enabled any more.
        #
        x = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.TEST(not x.is_enabled(), 
                        "Send button is not enabled after target number is supplied, but message still empty.")

