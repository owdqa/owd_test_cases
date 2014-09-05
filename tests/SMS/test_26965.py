#===============================================================================
# 26965: Verify in a sent SMS thread view that only valid URL appears
# highlighted
#
# Procedure:
# 1. Send from Device under Test to another device an SMS including a
# valid URL expression (f.e. "http://www.wikipedia.org/")
# 2. Open in Device under Test the SMS APP
# 3. Search and tap on the sent SMS
#
# Expected results:
# The valid URL expresion is shown highlighted in the SMS thread view
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

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
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.link = "www.wikipedia.org"
        self.test_msg = "Test with link: {} at {}".format(self.link, time.time())
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.network.getNetworkConnection()

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.phone_number], self.test_msg)

        #
        # Get the link of the first message
        #
        msg = self.UTILS.element.getElement(DOM.Messages.last_sent_message, "Last sent message")

        #
        # Verify that a valid URL appears highlight
        #
        y = msg.find_element("tag name", "a")
        self.UTILS.test.TEST(y.text == self.link, "The web link is highlighted in the text message")
