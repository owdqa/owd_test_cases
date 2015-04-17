#===============================================================================
# 29917: Verify that the user can delete an mms in a thread with several mms
#
# Procedure:
# 1. Open sms app
# 2. Open edit mode
# 3. Select a mms
# 4. Press delete button
#
# Expected results:
# The MMS is deleted
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg1 = "Hello World 1"
        self.test_msg2 = "Hello World 2"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.create_test_msgs([self.test_msg1, self.test_msg2])

        self.messages.openThread(self.phone_number)
        import time
        time.sleep(5)
        self.messages.deleteMessagesInThisThread([0])

        time.sleep(5)
        # After deleting one message, check there are three messages left
        msg_list = self.UTILS.element.getElements(DOM.Messages.message_list, "Remaining messages")
        self.UTILS.test.test(len(msg_list) == 3, "There are {} messages left (expected {})".format(len(msg_list), 3))

    def create_test_msgs(self, msgs):
        for msg in msgs:
            #
            # Create and Send a MMS.
            #
            self.messages.create_and_send_mms("image", [self.phone_number], msg)
            self.messages.wait_for_message()
            self.messages.closeThread()
