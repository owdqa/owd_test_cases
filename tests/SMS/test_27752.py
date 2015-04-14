#
# 27752: Receive an SMS with a link to a web site and open it
#
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(FireCTestCase):

    link = "www.google.com"
    test_msg = "Test " + link + " this."

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)

        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        last_msg = self.messages.last_message_in_this_thread()
        last_msg.find_element("tag name", "a").tap()

        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        self.UTILS.test.test(self.browser.check_page_loaded(self.link), "Web page loaded correctly.")
