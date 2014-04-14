#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery

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
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg1 = "Hello World 1"
        self.test_msg2 = "Hello World 2"

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], self.test_msg1)

        #
        # Back to send a new message
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], self.test_msg2)


        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread()

        #
        # Open the thread. This step is necessary because after sending a mms to 
        #our number two threads are created as a result.
        #
        x = self.UTILS.element.getElement(DOM.Messages.threads_list_element, 
                                    "+number Element")
        x.tap()

        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread()

        #
        # Verify that any thread is displayed.
        #
        self.UTILS.element.waitForElements(DOM.Messages.no_threads_message,
                                    "No message threads notification")
