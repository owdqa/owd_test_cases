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
        # Establish which phone number to use.
        #
        self.nums = [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM"),
                        self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")]

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
 
        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.createAndSendSMS(self.nums, "Test message")

        x = self.UTILS.element.getElements(DOM.Messages.thread_target_names, "Threads target names")

        bools = [title.text in self.nums for title in x]
        msgs = ["A thread exists for " + str(elem) for elem in self.nums]
        map(self.UTILS.test.TEST, bools, msgs)
