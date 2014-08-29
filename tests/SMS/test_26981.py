#
# 26981
#
from gaiatest import GaiaTestCase
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

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

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
        self.data_layer.send_sms(self.phone_number, "Email {} one.".format(self.emailAddy))
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.phone_number, timeout=120)
        self.UTILS.statusbar.click_on_notification_title(self.phone_number, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()
        #
        # Verify that the email address opens the email app.
        #
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

        sms = self.messages.lastMessageInThisThread()
        #
        # Verify that the email address does not open the email app.
        #
        link = sms.find_element("tag name", "a")
        link.tap()

        #
        # Now try to find the email app iframe.
        #
        time.sleep(2)
        self.wait_for_element_not_displayed(*DOM.Messages.header_send_message_btn, timeout=30)
