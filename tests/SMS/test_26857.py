#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Get the correct number for the sms device.
        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to a valid number to create a thread with just an
        # outgoing message
        #
        msg_text = str(time.time())
        self.messages.createAndSendSMS([self.num], msg_text)
        self.messages.waitForReceivedMsgInThisThread()

        #
        # Add another message to the same thread
        #
        msg_text = str(time.time())
        self.messages.enterSMSMsg(msg_text)
        self.messages.sendSMS()
        self.messages.waitForReceivedMsgInThisThread()

        #
        # Return to the threads view.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Get the preview txt for our test.
        #
        preview_text = self.messages.getThreadText(self.num)

        self.UTILS.test.TEST(preview_text in msg_text,
                        "Preview text (" + preview_text + ") is in the original message text(" + msg_text + ").")

