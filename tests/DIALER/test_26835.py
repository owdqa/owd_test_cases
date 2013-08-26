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
        self.dialer     = Dialer(self)
        
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        _num = "123456789"
        self.dialer.launch()
        
        self.dialer.enterNumber(_num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
        
        self.UTILS.toggleViaStatusBar("airplane")

        self.dialer.launch()
        self.dialer.openCallLog()
        
        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % _num),
                                   "The call log for number %s" % _num)
        x.tap()
        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_call, "Call button")
        x.tap()


        _warn = self.UTILS.getElement( ("xpath", "//p[contains(text(), 'airplane mode')]"), 
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Airplane mode warning displayed: \"%s\"" % _warn.text, x)
        
        
        x = self.UTILS.getElement( ("xpath", "//button[text()='OK']"), "OK button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")