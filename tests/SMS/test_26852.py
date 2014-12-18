#===============================================================================
# 26852: Delete a SMS in a conversation with several sms
#
# Procedure:
# 1- Send some sms to our device
# 2- Open SMS app
# 3- Open the conversation created with the last sms
# 4- Press edit button
# 5- Delete a SMS
#
# Expected results:
# The SMS is successfully deleted
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    test_msgs = ["First message", "Second message", "Third message"]

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
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        #
        # Launch messages app & delete all Threads
        # Make sure we have no threads
        #
        self.messages.launch()
        time.sleep(2)

        for i in range(3):
            self.UTILS.reporting.debug("** Sending [{}]".format(self.test_msgs[i]))
            self.data_layer.send_sms(self.phone_number, self.test_msgs[i])
            self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msgs[i], timeout=120)

        self.UTILS.reporting.debug("** Opening thread to check messages")
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.openThread(self.phone_number)

        #
        # Check how many elements are there
        #
        original_count = self.messages.countMessagesInThisThread()
        self.UTILS.reporting.logResult("info", "Before deletion there were {} messages in this thread.".\
                                       format(original_count))

        #
        # Select the messages to be deleted.
        #
        self.messages.deleteMessagesInThisThread([1])

        #
        # Check message isn't there anymore.
        #
        msg_list = self.UTILS.element.getElements(DOM.Messages.message_list, "Messages")
        final_count = len(msg_list)
        real_count = original_count - 1
        self.UTILS.test.test(final_count == (original_count - 1),
                        "After deleting the message, there were {} messages in this thread ({}) found).".\
                        format(real_count, final_count))
