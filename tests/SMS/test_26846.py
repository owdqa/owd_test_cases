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


class test_main(GaiaTestCase):

    test_msg = "First message."

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
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Make sure we have no threads
        #
        self.messages.deleteAllThreads()

        #
        # Create and send some new tests messages.
        #
        self.messages.createAndSendSMS([self.target_telNum], self.test_msg)
        self.messages.waitForReceivedMsgInThisThread()

        #
        # Go back..
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Delete this thread.
        #
        self.messages.deleteThreads([self.target_telNum])

        #
        # Check thread isn't there anymore.
        #
        self.UTILS.element.waitForNotElements(("xpath", DOM.Messages.thread_selector_xpath.format(self.target_telNum)),
                                      "Thread")
