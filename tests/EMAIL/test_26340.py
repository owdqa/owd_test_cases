#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from tests.EMAIL.shared_test_functions.emailing import Emailing


class test_26340(Emailing):

    _RESTART_DEVICE = True

    def setUp(self):
        self.testNum = self.__class__.__name__
        self.testType = "gmail"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.send_email()
