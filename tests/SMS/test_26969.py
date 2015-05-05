#===============================================================================
# 26969: Verify that when tapping on different valid URL's contained
# in the same SMS, the browser is opened each time with the selected URL
#
# Pre-requisites:
# Data or Wifi is enabled
#
# Procedure:
# ER1
# 1. Send from another device to the Device under Test an SMS including text
# and several valid URL expressions
# 2. Open in the Device under Test the SMS APP
# 3. Search and tap on the received SMS
# 4. In the SMS tap on one of the highlighted URL's
# 5. From the Browser App tap Home button to hide Browser App and return to
# Homescreen
# 6. Open again the SMS APP
# 7. Search and tap again on the received SMS
# 8. In the SMS tap on a different highlighted URL
# 9. Repeat steps from 5. to 8. till there aren't URL's not tried
# ER2
# 1. Long tap Home button
#
# Expected results:
# ER1
# The Browser APP is always opened with a new tab where the URL from the SMS
# is the one contained in the message.
# ER2
# Every URL opened is actived in each tab browser.
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(SpreadtrumTestCase):

    links = ["www.google.com", "www.hotmail.com", "www.wikipedia.org"]
    test_msg = "Test " + " ".join(links) + " this."

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        self.connect_to_network()

        # Create and send a new test message.
        self.data_layer.send_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)

        map(self.try_link, range(len(self.links)), self.links)

    def try_link(self, link_number, link):
        self.UTILS.reporting.logResult("info", "Tapping <b>{}</b> ...".format(link))

        # Switch to messaging app.
        self.messages.launch()
        self.messages.openThread(self.phone_number)
        time.sleep(1)

        # Get last message.
        msg = self.messages.last_message_in_this_thread()

        # Find all URLs
        l = msg.find_element("xpath", "//a[text()='{}']".format(link))

        # Tap on required link.
        self.UTILS.element.simulateClick(l)

        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(
            link in self.browser.loaded_url(), "Web page loaded #{} correctly.".format(link_number + 1))
