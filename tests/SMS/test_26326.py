
from gaiatest import GaiaTestCase
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
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.test_msg = "Test message."
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Start by making sure we have no other notifications.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)

        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)

        #
        # Click the notifier.
        #
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        self.messages.check_last_message_contents(self.test_msg)

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Check the message via the thread.
        #
        self.messages.openThread(title)
        self.messages.check_last_message_contents(self.test_msg)
