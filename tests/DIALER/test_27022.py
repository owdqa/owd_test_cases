#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()

        #
        # Open the call log and tap on the number.
        #
        self.apps.kill_all()
        time.sleep(3)
        self.dialer.launch()
        self.dialer.callLog_call(self.num)
