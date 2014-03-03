#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit import DOM
from OWDTestToolkit.apps import Settings, Dialer
#
# Imports particular to this test case.
#
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.settings = Settings(self)


         #
        # Get own number.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")


    def tearDown(self):


        self.UTILS.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()
        self.dialer.enterNumber("*31#")

         #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(2)

        self.UTILS.goHome()
        self.UTILS.logResult("info", "Home screen")

        #Tap settings
        self.settings.launch()
        self.UTILS.logResult("info", "Settings screen")

        x = self.UTILS.getElement(DOM.Settings.call_settings, "Call number button")
        x.tap()
        self.UTILS.logResult("info", "Call number presses")
        time.sleep(20)

        x = self.UTILS.getElement(DOM.Settings.call_button, "Call ID button")
        x.tap()
        self.UTILS.logResult("info", "Call ID button presses")

        #Change Frame
        self.marionette.switch_to_frame()

        #Get option selected
        x = self.UTILS.getElement(DOM.Settings.call_log_number_xpath, "Call Option value")
        y = x.get_attribute("aria-selected")

        self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)
        self.UTILS.TEST( y=="true", "Checking Call ID value")

