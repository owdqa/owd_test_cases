#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)

    
    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.launch()

        self.dialer.enterNumber("123456789")

        self.dialer.createContactFromThisNum()

