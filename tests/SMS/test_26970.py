#===============================================================================
# 26970: Verify that when tapping on the URL in the "Edit Mode",
# the Browser APP is not launched
#
# Procedure:
# 1. Send from another device to the Device under Test an SMS including text
# and a valid URL expression
# 2. Open in the Device under Test the SMS APP
# 3. Search and  tap on the received SMS
# 4. In the SMS thread view tap on the highlighted URL
# 4. In the SMS thread view tap in the right upper icon in order to change
# to "Edit Mode"
# 5. Tap on the URL
#
# Expected result:
# The Browser APP is  not launched by tapping. Only select and deselect
# messages are available options
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(GaiaTestCase):

    link = "www.google.com"
    test_msg = "Test " + link + " this."

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
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)

        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        msg = self.messages.wait_for_message()
        self.UTILS.test.test(msg, "Received a message.", True)

        # Go into messages Settings..
        #
        edit_btn = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        edit_btn.tap()

        select_btn = self.UTILS.element.getElement(DOM.Messages.edit_msgs_select_btn, "Select button")
        select_btn.tap()

        tag = msg.find_element("tag name", "a")
        tag.tap()

        header = self.UTILS.element.getElement(DOM.Messages.edit_msgs_header, "1 selected message")
        self.UTILS.test.test(header.text == "1 selected",
            "Into edit mode, if you tap on link, the browser is not open and the message is selected.")

        self.marionette.switch_to_frame()
        time.sleep(5)  # (give the browser time to launch)
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'browser')]"), "Browser iframe")
