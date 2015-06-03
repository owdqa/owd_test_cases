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

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.email = Email(self)

        self.email_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.email_address = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.emailAddy = self.UTILS.general.get_config_variable("gmail_2_email", "common")
        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.email.launch()
        self.email.setup_account(self.email_user, self.email_address, self.email_pass)

        # Create and send a new test message.
        self.messages.launch()
        test_msg = "Email address {} test at {}".format(self.emailAddy, time.time())
        self.data_layer.send_sms(self.phone_number, test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(test_msg, DOM.Messages.frame_locator)
        sms = self.messages.last_message_in_this_thread()

        # Verify that the email address opens the email app.
        link = sms.find_element("tag name", "a")
        link.tap()
        self.wait_for_element_displayed(*DOM.Messages.header_send_message_btn, timeout=30)

        cancel = self.UTILS.element.getElement(DOM.Messages.contact_cancel_btn, "Cancel button")
        cancel.tap()

        # Go into edit mode.
        edit_btn = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        edit_btn.tap()

        # Select Messages mode
        select_msgs_btn = self.UTILS.element.getElement(DOM.Messages.edit_msgs_select_btn, "Select messages button")
        select_msgs_btn.tap()
        self.UTILS.element.waitForElements(DOM.Messages.edit_msgs_header, "Edit messages mode header")

        # Verify that the email address does not open the email app.
        sms = self.messages.last_message_in_this_thread()
        link = sms.find_element("tag name", "a")
        link.tap()

        # Now try to find the email app iframe.
        self.wait_for_element_not_displayed(*DOM.Messages.header_send_message_btn, timeout=30)
