#
# 27752: Receive an SMS with a link to a web site and open it
#
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    link = "www.google.com"
    test_msg = "Test " + link + " this."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.connect_to_network()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        last_msg = self.messages.last_message_in_this_thread()
        last_msg.find_element("tag name", "a").tap()

        """
        Give the browser time to start up, then
        switch to the browser frame and check the page loaded.
        """
        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(
            self.link in self.browser.loaded_url(), "Web page loaded ({}) correctly.".format(self.link))
