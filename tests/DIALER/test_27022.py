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

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer      = Dialer(self)
        
        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()

        #self.marionette.switch_to_frame()
        #x = self.UTILS.getElement(DOM.Dialer.call_busy_button_ok, "OK button")
        #x.tap()

        time.sleep(2)
        self.dialer.hangUp()

        #
        # Open the call log and tap on the number.
        #
        self.apps.kill_all()
        time.sleep(3)
        self.dialer.launch()
        self.dialer.callLog_call(self.num)

     #   time.sleep(2)
     #   self.marionette.switch_to_frame()
     #   x = self.UTILS.getElement(DOM.Dialer.call_busy_button_ok, "OK button")
     #   x.tap()
        
        time.sleep(2)
        self.dialer.hangUp()

