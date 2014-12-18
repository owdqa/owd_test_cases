#===============================================================================
# 26844: Open SMS app after send and receive some SMS from different
# numbers (contacts and no contacts)
#
# Procedure:
# 1- Send some sms to our device from phone numbers who are contacts
# 1- Send some sms to our device from phone numbers who are not contacts
# 2- Opem SMS app
#
# Expected results:
# The user can see in the conversation list the number/contact the
# conversation was held with, the date/time of last message exchange and
# an excerpt of the last message exchanged
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use and set up the contact.
        #
        self.num1 = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.num1})

        self.UTILS.general.insertContact(self.contact)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        self.test_msg = "Test message at {}".format(time.time())

        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.create_and_send_sms([self.num1], self.test_msg)
        self.UTILS.messages.create_incoming_sms(self.num1, self.test_msg)
        self.messages.go_back()
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        incoming_num = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num,
                                                frame_to_change=DOM.Messages.frame_locator, timeout=5)

        # Check the threads for the required elements: name, time and excerpt
        for num in [self.contact["name"], incoming_num]:
            thread = self.UTILS.element.getElementByXpath(DOM.Messages.thread_selector_xpath.format(num))
            name = self.marionette.find_element(*DOM.Messages.threads, id=thread.id).text
            self.UTILS.test.test(num == name, "Expected thread name: {} Actual value: {}".format(num, name))
            thread_time = self.marionette.find_element('css selector', 'p.summary time', id=thread.id).text
            self.UTILS.test.test(thread_time, "Thread time found: {}".format(thread_time))
            excerpt = self.marionette.find_element('css selector', 'p.summary span.body-text', id=thread.id)
            self.UTILS.test.test(excerpt, "Thread excerpt found: {}".format(excerpt))
