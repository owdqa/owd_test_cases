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
from tests.mock_data.contacts import MockContacts
import time

class test_roy(GaiaTestCase):
    _Description = "(ignore me!)."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #self.messages.launch()
        
        #self.UTILS.wipeDeviceData(self)
        self.lockscreen.unlock()

        self.messages.launch()


