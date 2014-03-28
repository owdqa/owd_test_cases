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
from OWDTestToolkit.apps.email import Email
import time


class test_main(GaiaTestCase):

    test_msg = "Test message."
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.USER1 = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.EMAIL1 = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")
        self.PASS1 = self.UTILS.general.get_os_variable("GMAIL_1_PASS")

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Email addy {} test.".format(self.emailAddy))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the 2nd email link.
        #
        self.UTILS.reporting.logResult("info", "Click the email address in this message: '{}'.".format(x.text))
        _link = x.find_element("tag name", "a")
        _link.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        x.tap()

        time.sleep(4)
        self.marionette.switch_to_frame()

        x = self.UTILS.element.getElement(DOM.Email.confirm_ok, "Set up account confirmation")
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

        #
        # Try to set up the account - Since there is no connection, it will fail.
        #
        self.Email.setupAccountFirstStep(self.USER1, self.EMAIL1, self.PASS1)

        error = self.UTILS.element.getElement(DOM.Email.new_account_error_msg, "Error message")
        self.UTILS.test.TEST(error.text == "This device is currently offline. Connect to a network and try again.",
            "Verifying error message")
