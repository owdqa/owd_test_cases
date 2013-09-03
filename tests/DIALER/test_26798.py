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
from tests._mock_data.contacts import MockContacts
import time

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
        self.telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        self.UTILS.savePageHTML("/tmp/paloma.html")
        #
        # Enter a country prefix
        #
        self.dialer.enterNumber("0034"+self.telNum)
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()
        
        time.sleep(2)
        
        
        self.dialer.enterNumber("0039")
        
        
        #self.dialer.enterNumber("+34")
        
