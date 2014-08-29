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
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        _num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.dialer.launch()

        self.dialer.enterNumber(_num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        self.dialer.launch()
        self.dialer.openCallLog()

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(_num)),
                                   "The call log for number {}".format(_num))
        x.tap()
        x = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_call, "Call button")
        x.tap()

        _warn = self.UTILS.element.getElement(("xpath", "//p[contains(text(), 'airplane mode')]"),
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Airplane mode warning displayed: \"{}\"".format(_warn.text), x)

        x = self.UTILS.element.getElement(("xpath", "//button[text()='OK']"), "OK button")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")
