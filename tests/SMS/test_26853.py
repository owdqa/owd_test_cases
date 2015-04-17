from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(PixiTestCase):
    test_msgs = ["First message", "Second message", "Third message"]

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
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
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app & delete all Threads
        # Make sure we have no threads
        #
        self.messages.launch()

        for i in range(3):
            self.UTILS.reporting.debug("** Sending [{}]".format(self.test_msgs[i]))
            self.data_layer.send_sms(self.phone_number, self.test_msgs[i])
            self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msgs[i], timeout=120)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.openThread(self.phone_number)
        #
        # Go into edit mode..
        #
        x = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()

        #
        # Select Delete Messages
        #

        x = self.UTILS.element.getElement(DOM.Messages.delete_messages_btn, "Delete messages button")
        x.tap()

        #
        # Tap Selected all
        #
        x = self.UTILS.element.getElement(DOM.Messages.edit_msgs_sel_all_btn, "Select all button")
        x.tap()

        #
        # Tap delete
        #
        self.messages.deleteSelectedMessages()

        #
        # Check conversation isn't there anymore.
        #
        self.UTILS.element.waitForNotElements(("xpath",
            DOM.Messages.thread_selector_xpath.format(self.phone_number)), "Thread")

        time.sleep(1)
        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of final position:", fnam)
