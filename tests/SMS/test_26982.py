#===============================================================================
# 26982: Click on an email address in a sms who contains 3 emails
# addresses and verify the email in email app
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains 3 emails addresses
# 2. Open the thread view in the device A
# 3. click on the second email
# 4. Click on "Send email" button from the overlay
#
# Expected results:
# Email app is launched with the correct email charged in "to:" field
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.email_user = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.email_address = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")
        self.email_pass = self.UTILS.general.get_os_variable("GMAIL_1_PASS")

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Set up email account.
        #
        self.connect_to_network()

        self.Email.launch()
        self.Email.setupAccount(self.email_user, self.email_address, self.email_pass)

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        msg_text = "Email one one@tester.com, two {} , three three@tester.com at {}".\
                    format(self.emailAddy, time.time())
        self.data_layer.send_sms(self.phone_number, msg_text)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(msg_text, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(msg_text, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()
        time.sleep(1)

        #
        # Tap the 2nd email link.
        #
        self.UTILS.reporting.logResult("info", "Click the email address in this message: '{}'.".format(sms.text))
        _link = sms.find_elements("tag name", "a")[1]
        _link.tap()

        #
        # Click on "Send email" button from the overlay
        #
        send_btn = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        send_btn.tap()

        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.TEST(x.text == self.emailAddy,
                             "To field contains '{}' (it was '{}').".format(self.emailAddy, self.emailAddy))
