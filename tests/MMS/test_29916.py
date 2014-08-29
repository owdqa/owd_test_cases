#===============================================================================
# 29916: Verify that the user can delete all MMS in a thread with an unsent MMS
#
# Procedure:
# 1. Open SMS app
# 2. Open edit mode
# 3. Press select all button
# 4. Press delete button
#
# Expected results:
# All MMS are removed
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    # Restart device to starting with wifi and 3g disabled.
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
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and Send a MMS.
        #
        self.messages.createAndSendMMS("image", [self.phone_number], self.test_msg1)
        self.messages.closeThread()

        #
        # Create and Send another MMS.
        #
        self.messages.createAndSendMMS("image", [self.phone_number], self.test_msg2)
        self.messages.closeThread()

        #
        # Create and Send yet another MMS.
        #
        self.messages.createAndSendMMS("image", [self.phone_number], self.test_msg3)
        self.messages.openThread(self.phone_number)
        self.messages.deleteMessagesInThisThread()
