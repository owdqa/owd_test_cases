#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):

   #
    # Restart device to starting with wifi and 3g disabled.
    #
    _RESTART_DEVICE = True


    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        #With format= +34 xxxxxxxxx
        self.test_num_1 = "620972162"
        self.test_num_2 = "0034620972162"
        self.test_num_3 = "+34620972162"


    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        self.messages.launch()

        #
        # Create and Send an MMS
        #
        self.messages.createAndSendMMS("image", [self.test_num_1], self.test_msg)
        #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.test_num_2], self.test_msg)
          #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        self.messages.createAndSendMMS("image", [self.test_num_3], self.test_msg)
          #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        #
        # Check how many elements are there
        #
        self.UTILS.reporting.logResult("info", "Check how many threads are there")
        original_count = self.messages.countNumberOfThreads()
        self.UTILS.reporting.logResult("info",
                             "Number of threads " + str(original_count) +
                              " in list.")
        self.UTILS.test.TEST(original_count == 1, "Check how many threads are there")
