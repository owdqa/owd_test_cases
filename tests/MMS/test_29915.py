#===============================================================================
# 29915: Send a mms to a number using different prefixes (00, +XX)
# and verify that only a thread is created
#
# Procedure:
# 1. Send a MMS to a number 0034 xxxxxxxxx
# 2. Send another MMS to the same number: +34 xxxxxxxxx
# 3. Send a third message to the same number without country code: xxxxxxxxx
#
# Expected results:
# Only one thread is created
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

        # Define target phone numbers
        num_prefix_plus = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        num_prefix_double_zero = num_prefix_plus.replace("+", "00")
        num_no_prefix = num_prefix_plus.replace("+34", "")
        self.target_numbers = [num_prefix_plus, num_prefix_double_zero, num_no_prefix]
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        for num in self.target_numbers:
            test_msg = "Hello World at {} for {}".format(time.time(), num)
            self.messages.create_and_send_mms("image", [num], test_msg)
            self.messages.wait_for_message()
            self.messages.closeThread()
            time.sleep(3)

        #
        # Check how many elements are there
        #
        count = self.messages.countNumberOfThreads()
        self.UTILS.reporting.logResult("info", "Number of threads {} in list.".format(count))
        self.UTILS.test.TEST(count == 1, "There are {} threads (expected {})".format(count, 1))
