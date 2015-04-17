#===============================================================================
# 26981: Verify that an user cannot click on an email address in the edit mode
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Open the thread view in the device A
# ER1
# 3. Open edit mode
# ER2
#
# Expected results:
# ER1 will be highlighted for each email address
# ER2 will not be highlighted for each email address and the user can't click on it
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.email_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.email_address = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.emailAddy = self.UTILS.general.get_config_variable("gmail_2_email", "common")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
        test_msg = "Email address {} test at {}".format(self.emailAddy, time.time())
        self.data_layer.send_sms(self.phone_number, test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(test_msg, DOM.Messages.frame_locator)
        sms = self.messages.last_message_in_this_thread()
        #
        # Verify that the email address opens the email app.
        #
        time.sleep(2)
        link = sms.find_element("tag name", "a")
        link.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.wait_for_element_displayed(*DOM.Messages.header_send_message_btn, timeout=30)
        cancel = self.UTILS.element.getElement(DOM.Messages.contact_cancel_btn, "Cancel button")
        cancel.tap()

        #
        # Go into edit mode.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()
        delete_btn = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete messages button")
        delete_btn.tap()

        sms = self.messages.last_message_in_this_thread()
        #
        # Verify that the email address does not open the email app.
        #
        time.sleep(2)
        link = sms.find_element("tag name", "a")
        link.tap()

        #
        # Now try to find the email app iframe.
        #
        time.sleep(2)
        self.wait_for_element_not_displayed(*DOM.Messages.header_send_message_btn, timeout=30)
