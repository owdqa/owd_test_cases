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
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.dialer = Dialer(self)
        self.settings = Settings(self)



    def tearDown(self):


        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Calls the current number.
        #

        self.dialer.launch()
        self.dialer.enterNumber("#31#")
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(2)

        self.UTILS.home.goHome()
        self.UTILS.reporting.logResult("info", "Home screen")

        #Tap settings
        self.settings.launch()
        self.UTILS.reporting.logResult("info", "Settings screen")

        self.settings.callID_verify()


        self.UTILS.home.goHome()
        self.UTILS.reporting.logResult("info", "Home screen")


        self.dialer.launch()
        self.dialer.enterNumber("*#31#")

     #
        # Calls the current number.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(2)

        self.UTILS.home.goHome()
        self.UTILS.reporting.logResult("info", "Home screen")

        #Tap settings
        self.settings.launch()
        self.UTILS.reporting.logResult("info", "Settings screen")

        self.settings.callID_verify()
