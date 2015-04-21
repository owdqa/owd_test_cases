#===============================================================================
# 26978: Click on an email address and send an email (any email account
# configured in the email app)(gmail account)
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Open the thread view in the device A
# 3. Click on the email address
# 4. Tap on "Send email" button from the overlay
# ER1
# 5. Confirm we want to configure an email account
# 6. configure an gmail acount
# ER2
# 7. write a email text
# 8. Press send button
# ER3
#
# Expected results:
# ER1. email app is launched to configure an email acount
# ER2. new message screen is launched with the email charged in the "to:" label
# ER3. the email is sent
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
import time


class test_main(PixiTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.email = Email(self)

        self.email_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.email_address = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.dest_email = self.UTILS.general.get_config_variable("gmail_2_email", "common")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up email account.
        #
        self.connect_to_network()

        #
        # Create and send a new test message.
        #
        test_msg = "email address {} test at {}".format(self.dest_email, time.time())
        self.data_layer.send_sms(self.phone_number, test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(test_msg, DOM.Messages.frame_locator)
        sms = self.messages.last_message_in_this_thread()
        time.sleep(1)

        #
        # Tap the 2nd email link.
        #
        self.UTILS.reporting.logResult("info", "Click the email address in this message: '{}'.".format(sms.text))
        _link = sms.find_element(*DOM.Messages.email_info_in_msg)
        self.UTILS.element.simulateClick(_link)

        #
        # Tap on "Send email" button from the overlay
        #
        send_btn = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        send_btn.tap()

        time.sleep(4)
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        #
        # Confirm we want to setUp our email account
        #
        ok_btn = self.UTILS.element.getElement(DOM.Email.email_not_setup_ok, "Set up account confirmation")
        ok_btn.tap()

        self.email.setupAccount(self.email_user, self.email_address, self.email_pass)

        #
        # Verify the email address is in the To field.
        #
        to_field = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.test(to_field.text == self.dest_email,
                             "To field contains '{0}' (it was '{0}').".format(self.dest_email))

        #
        # Fill in the details and send the email.
        #
        self.UTILS.general.typeThis(DOM.Email.compose_subject, "'Subject' field", "Test email", True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", "Just a test", True, False, False)

        send_btn = self.UTILS.element.getElement(DOM.Email.compose_send_btn, "Send button")
        send_btn.tap()
        self.UTILS.element.waitForNotElements(DOM.Messages.send_email_failed, "Sending email error message",
                                              timeout=10)
