#===============================================================================
# 26847: Select some conversations and press delete
#
# Procedure:
# 1- Access to SMS app
# 2- Press edit button
# 3- Select multiple conversations
# 4- Press delete button
#
# Expected result:
# The selected conversations are successfully deleted
#===============================================================================

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')

        #
        # Import details of our test contacts.
        #
        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[0]["tel"] = {'type': 'Mobile', 'value': self.phone_number}
        self.test_contacts[1]["tel"] = {'type': 'Mobile', 'value': self.incoming_sms_num[0]}
        self.test_contacts[2]["tel"] = {'type': 'Mobile', 'value': self.incoming_sms_num[1]}

        map(self.UTILS.general.insertContact, self.test_contacts)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.UTILS.reporting.debug("*** Sending SMS to {}".format(self.test_contacts[0]["tel"]["value"]))
        self.messages.create_and_send_sms([self.test_contacts[0]["tel"]["value"]], self.test_msg)
        back_btn = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        back_btn.tap()

        for i in range(2):
            self.test_msg = "Test message {} at {}".format(i, time.time())
            self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
            self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Delete all threads, except the last one.
        #
        self.messages.threadEditModeON()
        edit_btn = self.UTILS.element.getElement(DOM.Messages.edit_threads_button, "Edit threads button")
        edit_btn.tap()

        delete_threads_btn = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        delete_threads_btn.tap()

        thread_list = self.UTILS.element.getElements(DOM.Messages.threads_list, "Message threads")
        for i in range(len(thread_list) - 1):
            thread_list[i].tap()

        self.messages.deleteSelectedThreads()

        #
        # Check there is now only 1 thread.
        #
        msgs = self.UTILS.element.getElements(DOM.Messages.threads_list, "Message threads after deletion")
        self.UTILS.test.test(len(msgs) == 1, "Only 1 thread is left after deleting the other two.")
