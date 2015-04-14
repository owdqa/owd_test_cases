#===============================================================================
# 26983: Click on an email address when data and wifi are off
#
# Pre-requisites:
# Data and wifi are off
#
# Procedure:
# 1. Send a sms from "device A" to "device B" which contains an email address
# 2. Open the thread view in the device A
# 3. Click on the email address
# 4. Select "Send email" option from the overlay
# 5. Select "OK" to confirm the setup of an email account
# 6. Fill the formulary
# 7. Click on "Next" button
#
# Expected results:
# There should be an error message to warn user that a connection is needed
#===============================================================================

import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
from tests.i18nsetup import setup_translations


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.email = Email(self)

        self.email_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.email_address = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.dest_email = self.UTILS.general.get_config_variable("gmail_2_email", "common")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common")
        _ = setup_translations(self)
        self.expected_error_message = _(
            'Unable to establish a connection with "imap.googlemail.com". There may be a problem with the network.')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
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
        self.UTILS.reporting.logResult("info", u"Click the email address in this message: '{}'.".format(sms.text))
        _link = sms.find_element("tag name", "a")
        _link.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        x.tap()

        time.sleep(4)

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.email_not_setup_ok, "Set up account confirmation")
        x.tap()

        #
        # Try to set up the account - Since there is no connection, it will fail.
        #
        self.email.setupAccountFirstStep(self.email_user, self.email_address, self.email_pass)

        error = self.UTILS.element.getElement(DOM.Email.new_account_error_msg, "Error message")
        self.UTILS.test.test(error.text == self.expected_error_message, "Verifying error message")
