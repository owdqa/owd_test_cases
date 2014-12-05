#===============================================================================
# 26966: Verify in a received SMS thread view that only valid URL appears
# highlighted
#
# Procedure:
# 1. Send from another device to the Device under Test an SMS including
# a valid URL expression (f.e. "http://www.wikipedia.org/")
# 2. Open in the Device under Test the SMS APP
# 3. Search and tap on the received SMS
#
# Expected results:
# The valid URL expression is shown highlighted in the SMS thread view
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.link = "www.wikipedia.org"
        self.test_msg = "Test with link {} at {}".format(self.link, time.time())
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(self.test_msg, frame_to_change=DOM.Messages.frame_locator)
        self.UTILS.reporting.debug("Checking last message in thread")

        #
        #Verify that a valid URL appears highlight
        #
        msg = self.messages.last_message_in_this_thread()
        y = msg.find_element("tag name", "a")
        self.UTILS.test.test(y.text == self.link, "The web link is highlighted in the text message")
