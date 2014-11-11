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
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.corporate_sim = self.UTILS.general.get_os_variable("CORPORATE_SIM") == "True"
        self.UTILS.test.test(self.corporate_sim, "Using a corporate SIM. The test can continue", True)

        #
        # Establish which phone number to use.
        #
        self.nums = [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM"),
                        self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")]
        self.own_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Make sure we have no contacts.
        #
        self.data_layer.remove_all_contacts()

        #
        # Launch messages app.
        #
        self.messages.launch()

        for num in self.nums:
            test_msg = "Test message at {} for {}".format(time.time(), num)
            self.messages.createAndSendSMS([num], test_msg)
            if num == self.own_number:
                send_time = self.messages.last_sent_message_timestamp()
                self.messages.wait_for_message(send_time=send_time)
            else:
                self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)
                self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
            back_btn = self.marionette.find_element(*DOM.Messages.header_back_button)
            back_btn.tap()

        x = self.UTILS.element.getElements(DOM.Messages.thread_target_names, "Threads target names")

        bools = [title.text in self.nums for title in x]
        msgs = ["A thread exists for {}".format(elem) for elem in self.nums]
        map(self.UTILS.test.test, bools, msgs)
