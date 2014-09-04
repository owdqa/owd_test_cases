#===============================================================================
# 26843: Open SMS app after send and receive some SMS from different
# numbers (contacts)
#
# Procedure:
# 1- Send some sms to phone numbers who are contacts
# 2- Send some sms to our device from phone numbers who are contacts
# 2- Opem SMS app
#
# Expected results:
# The SMS app shows a list with all conversations held is displayed
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use and set up the contacts.
        #
        self.nums = [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM"),
                        self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")]

        self.test_contacts = [MockContact(tel={'type': 'Mobile', 'value': num}) for num in self.nums]
        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.createAndSendSMS(self.nums, "Test message")

        thread_names = self.UTILS.element.getElements(DOM.Messages.thread_target_names, "Threads target names")

        contacts_names = [elem["name"] for elem in self.test_contacts]
        bools = [title.text in contacts_names for title in thread_names]

        msgs = ["A thread exists for {}".format(elem) for elem in contacts_names]
        map(self.UTILS.test.TEST, bools, msgs)
