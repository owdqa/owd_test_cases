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
        self.incoming_sms_num = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Set up email account.
        #
        self.UTILS.network.getNetworkConnection()

        #
        # Create and send a new test message.
        #
        send_time = time.time()
        #self.UTILS.messages.create_incoming_sms(self.num1, "Email addy {} test.".format(self.emailAddy))
        self.data_layer.send_sms(self.num1, "Email addy {} test.".format(self.emailAddy))
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.num1, timeout=120)
        self.UTILS.statusbar.click_on_notification_title(self.num1, DOM.Messages.frame_locator)
        sms = self.messages.waitForReceivedMsgInThisThread(send_time=send_time)

        #
        # Tap the 2nd email link.
        #
        self.UTILS.reporting.logResult("info", "Click the email address in this message: '{}'.".format(sms.text))
        _link = sms.find_element("tag name", "a")
        _link.tap()

        #
        # Tap on "Send email" button from the overlay
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        x.tap()

        time.sleep(4)
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        #
        # Confirm we want to setUp our email account
        #
        x = self.UTILS.element.getElement(DOM.Email.email_not_setup_ok, "Set up account confirmation")
        x.tap()

        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)

        #
        # Verify the email address is in the To field.
        #
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.TEST(x.text == self.emailAddy,
                        "To field contains '{0}' (it was '{0}').".format(self.emailAddy))

        #
        # Fill in the details and send the email.
        #
        self.UTILS.general.typeThis(DOM.Email.compose_subject, "'Subject' field", "Test email", True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", "Just a test", True, False, False)

        self.Email.sendTheMessage()
