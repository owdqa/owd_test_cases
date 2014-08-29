#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
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
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        _num = "123456789"
        self.dialer.launch()
        self.dialer.enterNumber(_num)
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        _warn = self.UTILS.element.getElement( ("xpath", "//p[contains(text(), 'airplane mode')]"), 
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Airplane mode warning displayed: \"%s\"" % _warn.text, x)


        x = self.UTILS.element.getElement( ("xpath", "//button[text()='OK']"), "OK button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.test.TEST(str(_num) in dialer_num, "After cancelling, phone number field still contains '%s' (it was '%s')." % \
                                                       (_num,dialer_num))
