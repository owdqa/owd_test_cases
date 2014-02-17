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
    _RESTART_DEVICE = True

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
        self._TestMsg3    = "Hello World 3"


        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        val=2

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
        # Create and Send other MMS.
        #
        self.messages.createAndSendMMS("image", self._TestMsg2)

        #
        # Back to send a new sms
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and Send other MMS.
        #
        self.messages.createAndSendMMS("image", self._TestMsg3)


        #
        # Create reference in xpth with value "val".
        #
        a=(DOM.Messages.message_text[0],DOM.Messages.message_text[1]%val)
        elem1 = self.UTILS.getElement(a, "mms text")
        header1=elem1.text


        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread([1])


        #
        # Create reference in xpth with value "val".
        #
        b=(DOM.Messages.message_text[0],DOM.Messages.message_text[1]%val)
        elem2 = self.UTILS.getElement(a, "mms text")
        header2=elem2.text

        #
        # Vary that header[1] is different after deleting a message".
        #
        self.UTILS.TEST(header1 != header2, "HEADER BEFORE DETELING A MMS: " + header1 + " HEADER AFTER DETELING A MMS: " + header2, True)



