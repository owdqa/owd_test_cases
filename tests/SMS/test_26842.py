#===============================================================================
# 26842: Open SMS app after send and receive some SMS from different
# numbers (no contacts)
#
# Procedure:
# 1- Send some sms to phone numbers who are not contacts
# 2- Send some sms to our device from phone numbers who are not contacts
# 2- Opem SMS app
#
# Expected results:
# The SMS app shows a list with all conversations held
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.own_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.nums = [self.own_number, self.UTILS.general.get_config_variable("short_phone_number", "custom")]
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.remove_all_contacts()

        # Launch messages app.
        self.messages.launch()

        for num in self.nums:
            test_msg = "Test message at {} for {}".format(time.time(), num)
            self.messages.create_and_send_sms([num], test_msg)
            if num == self.own_number:
                send_time = self.messages.last_sent_message_timestamp()
                self.messages.wait_for_message(send_time=send_time)
            else:
                self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
                self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
            self.messages.go_back()

        target_names = self.UTILS.element.getElements(DOM.Messages.thread_target_names, "Threads target names")

        bools = [title.text in self.nums for title in target_names]
        msgs = ["A thread exists for {}".format(elem) for elem in self.nums]
        map(self.UTILS.test.test, bools, msgs)
