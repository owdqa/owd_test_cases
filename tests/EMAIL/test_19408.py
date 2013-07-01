#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests.shared_test_functions import EMAILING

class test_19408(EMAILING.main):
    _Description = "[BASIC][EMAIL] Receive email with hotmail."
    
    def setUp(self):
        self.testNum  = self.__class__.__name__
        self.testType = "hotmail"

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.receive_email()
