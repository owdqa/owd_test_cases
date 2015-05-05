#===============================================================================
# 26853: Delete all SMS in a conversation with several sms
#
# Procedure:
# 1- Send some sms to our device
# 2- Open SMS app
# 3- Open the conversation created with the last sms
# 4- Press edit button
# 5- Press Select all button
# 6- Press Delete button
# 7- Press OK
#
# Expected results:
# All SMS are deleted successfully and the conversation is deleted
# automatically
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(SpreadtrumTestCase):
    test_msgs = ["First message", "Second message", "Third message"]

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        """
        Launch messages app & delete all Threads
        Make sure we have no threads
        """

        self.messages.launch()

        for i in range(3):
            self.UTILS.reporting.debug("** Sending [{}]".format(self.test_msgs[i]))
            self.data_layer.send_sms(self.phone_number, self.test_msgs[i])
            self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msgs[i], timeout=120)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.openThread(self.phone_number)

        # Go into edit mode..
        edit_btn = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        edit_btn.tap()

        select_btn = self.UTILS.element.getElement(DOM.Messages.edit_msgs_select_btn, "Select messages button")
        select_btn.tap()

        # Select all
        select_all_btn = self.UTILS.element.getElement(DOM.Messages.check_all_messages_btn, "Select all button")
        select_all_btn.tap()

        # Tap delete
        self.messages.deleteSelectedMessages()

        # Check conversation isn't there anymore.
        self.UTILS.element.waitForNotElements(("xpath",
            DOM.Messages.thread_selector_xpath.format(self.phone_number)), "Thread")

        time.sleep(1)
        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of final position:", fnam)
