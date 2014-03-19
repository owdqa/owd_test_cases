#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test message."

    _RESTART_DEVICE = True

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
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        self.Contact_1 = MockContact(tel={'type': 'Mobile', 'value': self.num1})

        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.createAndSendSMS([self.num1, self.num2], "Test message")

        # Waiting for the replies isn't really part of the test, so just continue...

        x = self.UTILS.element.getElements(DOM.Messages.threads_list, "Threads")

        bool_1_target_ok = False
        bool_2_target_ok = False
        bool_1_time_ok = False
        bool_2_time_ok = False
        bool_1_snippet_ok = False
        bool_2_snippet_ok = False
        counter = 1
        for i in x:
            #
            # Target details.
            #
            y = i.find_element('xpath', './/p[@class="name"]')
            self.UTILS.reporting.logResult("info", "Thread target: " + y.text)
            if y.text == self.Contact_1["name"]:
                bool_1_target_ok = True
            if y.text == self.num2:
                bool_2_target_ok = True

            #
            # Time details.
            #
            y = i.find_element('tag name', 'time')
            self.UTILS.reporting.logResult("info", "Thread time: " + y.text)
            if counter == 1:
                bool_1_time_ok = True
            else:
                bool_2_time_ok = True

            #
            # Conversation snippet details.
            #
            y = i.find_element('xpath', './/span[@class="body-text"]')
            self.UTILS.reporting.logResult("info", "Thread conversation snippet: " + y.text)
            if counter == 1:
                bool_1_snippet_ok = True
            else:
                bool_2_snippet_ok = True

            #
            # Increment the counter.
            #
            counter = counter + 1

        self.UTILS.test.TEST(bool_1_target_ok, "A thread exists for target " + self.Contact_1["name"])
        self.UTILS.test.TEST(bool_2_target_ok, "A thread exists for target " + str(self.num2))

        self.UTILS.test.TEST(bool_1_time_ok, "A timestamp exists for thread 1.")
        self.UTILS.test.TEST(bool_2_time_ok, "A timestamp exists for thread 2.")

        self.UTILS.test.TEST(bool_1_snippet_ok, "A conversation snippet exists for thread 1.")
        self.UTILS.test.TEST(bool_2_snippet_ok, "A conversation snippet exists for thread 2.")
