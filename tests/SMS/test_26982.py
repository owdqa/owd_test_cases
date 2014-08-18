#
# 26982
#
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email


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

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Set up email account.
        #
        self.UTILS.network.getNetworkConnection()

        self.Email.launch()
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        msg_text = "Email one one@tester.com, two {} , three three@tester.com.".format(self.emailAddy)
        self.data_layer.send_sms(self.phone_number, msg_text)
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.phone_number, timeout=120)
        self.UTILS.statusbar.click_on_notification_title(self.phone_number, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()

        #
        # Tap the 2nd email link.
        #
        self.UTILS.reporting.logResult("info", "Click the 2nd email address in this message: '{}'.".format(sms.text))
        _link = sms.find_elements("tag name", "a")[1]
        _link.tap()

        #
        # Click on "Send email" button from the overlay
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        x.tap()

        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.TEST(x.text == self.emailAddy,
                             "To field contains '{}' (it was '{}').".format(self.emailAddy, self.emailAddy))
