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
from OWDTestToolkit.apps.settings import Settings
import time

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
        self.Settings = Settings(self)

        self.test_msg = "Hello World"

          #
        # Import contact (adjust the correct number).
        #
        self._num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self._num)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
            #
        # Launch messages app.
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
        self.messages.launch()

        #
        # Create and Send an MMS
        #
        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], "Test 1")
         #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], "Test 2")
         #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], "Test 3")
         #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        #
        # Enter the thread.
        #
        self.messages.openThread(self._num)

        #
        # Find the first message.
        #
        x = self.UTILS.element.getElements(DOM.Messages.message_list, "Message list", False)
        pos = 0
        for i in x:

            # Do the check of each message.
            #
            self.UTILS.test.TEST(i.find_element("xpath", ".//p").text == "Test {}".format(pos + 1),
                        "The messages at position " + str(pos) + " contains the string '" + "Test {}".format(pos + 1) + "'.")
            self.UTILS.test.TEST("outgoing" in i.get_attribute("class"),
                        "The message at position " + str(pos) + " is  outgoing.")
            pos += 1
