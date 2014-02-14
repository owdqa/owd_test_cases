#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *


class test_main(GaiaTestCase):

    #
    # Restart device to starting with wifi and 3g disabled.
    #
    #_RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.gallery    = Gallery(self)
        self.Settings   = Settings(self)
        self._TestMsg1    = "Hello World 1"
        self._TestMsg2    = "Hello World 2"


        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):


        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", self._TestMsg1)

        #
        # Back to send a new sms
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", self._TestMsg2)


        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread()

        #
        # Open the thread. This step is necessary because after send a mms to our number are created two threads .
        #
        x = self.UTILS.getElement(DOM.Messages.threads_list_element, "+number Element")
        x.tap()

        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread()

        #
        # Verify that any thread is displayed.
        #
        self.UTILS.waitForElements(DOM.Messages.no_threads_message, "No message threads notification")
