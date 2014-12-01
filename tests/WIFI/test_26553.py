#===============================================================================
# 26553: Receiving SMS during a Wi-Fi session
#
# Pre-requisites:
# There should be a Wi-Fi network available to connect to.
# Another device to send messages to our device is also needed
#
# Procedure:
# 1- Make a WiFi connection.
# 2- Launch a WEB browsing session over Wi-Fi
# 3- Send a SMS from another mobile to our device under test. Check
# the SMS is received correctly
# 4- Check that the Wi-Fi connection remains active. Confirm browsing
# to another WEB page.
#
# Expected results:
# The SMS must be correctly received by the device under test and the
# Wi-Fi connection must remain active.
#===============================================================================
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.browser = Browser(self)
        self.messages = Messages(self)

        self.num = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("GLOBAL_CP_NUMBER").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()
        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url("www.google.com")

        test_msg = "This is a test message sent at {} while connected to a wifi".format(time.time())
        self.UTILS.messages.create_incoming_sms(self.num, test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(test_msg, DOM.Messages.frame_locator)
        self.messages.check_last_message_contents(test_msg)

        self.browser.launch()
        self.browser.open_url("www.wikipedia.com")
        self.UTILS.test.test(self.browser.check_page_loaded("www.wikipedia.com"), "Web page loaded correctly.")
