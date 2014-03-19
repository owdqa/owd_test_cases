#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    test_msg = "Test message."

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
        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.msg = "Test " + str(time.time())

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        self.UTILS.reporting.logResult("info", "** TEST: receive msg while in the thread.")
        self.messages.createAndSendSMS([self.num], "Test message")
        self.messages.waitForReceivedMsgInThisThread()

        # Do this 'long hand' so we can switch back to the main screen before the message finishes
        # sending (or we might miss the return notification).
        self.UTILS.reporting.logResult("info", "** TEST: receive msg while in main screen (looking at threads).")
        self.messages.enterSMSMsg(self.msg)
        x = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.waitForNewSMSPopup_by_msg(self.msg)
