#===============================================================================
# 26552: Sending SMS during a Wi-Fi session
#
# Pre-requisites:
# There should be a Wi-Fi network available to connect to.
# Another device to send messages to is also needed
#
# Procedure:
# 1- Make a WiFi connection.
# 2- Launch a WEB browsing session over Wi-Fi
# 3- Send a SMS to another mobile. Check that the SMS was received by another
# mobile
# 4- Check that the Wi-Fi connection remains active. Confirm browsing to
# another WEB page.
#
# Expected results:
# The SMS must be correctly received by another mobile and the Wi-Fi connection
# must remain active.
#===============================================================================

from gaiatest import GaiaTestCase
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

        self.num = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.url1 = "www.google.com"
        self.url2 = "www.wikipedia.org"
        self.test_msg = "Test message"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        # Open the first url
        self.browser.launch()
        self.browser.open_url(self.url1)
        self.UTILS.test.test(self.browser.check_page_loaded(self.url1), "{} successfully loaded".format(self.url1))

        #
        # Open the SMS app, send a message then jump back to the browser.
        #
        self.messages.launch()
        self.messages.create_and_send_sms([self.num], self.test_msg)
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.wait_for_message(send_time)

        self.apps.kill_all()

        self.browser.launch()
        self.browser.open_url(self.url2)
        self.UTILS.test.test(self.browser.check_page_loaded(self.url2), "{} successfully loaded".format(self.url2))
