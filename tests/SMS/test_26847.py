#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
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
        tel = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Import details of our test contacts.
        #
        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[0]["tel"] = {'type': 'Mobile', 'value': tel}

        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Make sure we have no threads
        #
        self.messages.deleteAllThreads()

        #
        # Create and send a new test message.
        #
        for i in range(len(self.test_contacts)):

            self.messages.createAndSendSMS([self.test_contacts[i]["tel"]["value"]], self.test_msg)
            x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

        #
        # Delete all threads, except the last one.
        #
        self.messages.threadEditModeON()
        x = self.UTILS.element.getElement(DOM.Messages.edit_threads_button, "Edit threads button")
        x.tap()

        delete_threads_btn = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        delete_threads_btn.tap()

        x = self.UTILS.element.getElements(DOM.Messages.threads_list, "Message threads")
        for i in range(len(x) - 1):
            x[i].tap()

        self.messages.deleteSelectedThreads()

        #
        # Check there is now only 1 thread.
        #
        x = self.UTILS.element.getElements(DOM.Messages.threads_list, "Message threads after deletion")
        self.UTILS.test.TEST(len(x) == 1, "Only 1 thread is left after deleting the other two.")
