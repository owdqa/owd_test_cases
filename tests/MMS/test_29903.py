#===============================================================================
# 29903: Verify that all the MMSs in a thread are chronologically ordered
#
# Procedure:
# On DuT create an MMS thread by sending/receiving MMSs to/from the same number
#
# Expected results:
# All the MMSs in the same thread are correctly ordered no matter the time set
# in one device or the other or the network
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

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
        self.settings = Settings(self)

        self.test_msg = "Hello World"

        #
        # Import contact (adjust the correct number).
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
            #
        # Launch messages app.
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
        self.messages.launch()

        #
        # Create and Send an MMS
        #
        self.messages.createAndSendMMS("image", [self.phone_number], "Test 1")
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.phone_number], "Test 2")
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.phone_number], "Test 3")
        self.messages.closeThread()

        #
        # Enter the thread.
        #
        self.messages.openThread(self.phone_number)

        #
        # Find the first message.
        #
        x = self.UTILS.element.getElements(DOM.Messages.message_list, "Message list", False)
        pos = 0
        for i in x:
            # Do the check of each message.
            #
            self.UTILS.test.TEST(i.find_element("xpath", ".//p/span").text == "Test {}".format(pos + 1),
                        "The message at position {} contains the string 'Test {}'.".format(pos, pos + 1))
            self.UTILS.test.TEST("outgoing" in i.get_attribute("class"),
                        "The message at position " + str(pos) + " is  outgoing.")
            pos += 1
