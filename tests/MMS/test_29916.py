#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery

class test_main(GaiaTestCase):

    #
    # Restart device to starting with wifi and 3g disabled.
    #
    _RESTART_DEVICE = True

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
        self.test_msg3 = "Hello World 3"

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        val=2

        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", self.test_msg1)

        #
        # Back to send a new message
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and Send other MMS.
        #
        self.messages.createAndSendMMS("image", self.test_msg2)

        #
        # Back to send a new message
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and Send other MMS.
        #
        self.messages.createAndSendMMS("image", self.test_msg3)


        #
        # Create reference in xpth with value "val".
        #
        locator = (DOM.Messages.message_text[0],
                    DOM.Messages.message_text[1].format(val))

        elem1 = self.UTILS.element.getElement(locator, "mms text")
        header1 = elem1.text


        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread([1])


        #
        # Create reference in xpth with value "val".
        #
        elem2 = self.UTILS.element.getElement(locator, "mms text")
        header2 = elem2.text

        #
        # Vary that header[1] is different after deleting a message".
        #
        self.UTILS.test.TEST(header1 != header2, 
            "HEADER BEFORE DETELING A MMS: " + header1 + " HEADER AFTER DETELING A MMS: " + header2, True)




