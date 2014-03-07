#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.toggleViaStatusBar("airplane")
        
        _num = "123456789"
        self.dialer.launch()
        self.dialer.enterNumber(_num)
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        _warn = self.UTILS.getElement( ("xpath", "//p[contains(text(), 'airplane mode')]"), 
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Airplane mode warning displayed: \"%s\"" % _warn.text, x)
        
        
        x = self.UTILS.getElement( ("xpath", "//button[text()='OK']"), "OK button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.TEST(str(_num) in dialer_num, "After cancelling, phone number field still contains '%s' (it was '%s')." % \
                                                       (_num,dialer_num))
