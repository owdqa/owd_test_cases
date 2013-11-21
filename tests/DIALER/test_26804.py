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

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

        #self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cont_twilio = MockContacts().Contact_twilio
        self.num = self.cont_twilio["tel"]["value"]

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        
        self.dialer.callThisNumber()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of call being made with mute and speaker off:", x)
        
        self.dialer.hangUp()
        
