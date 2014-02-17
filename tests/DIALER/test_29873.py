#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import *
#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts
import time


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)
        self.settings   = Settings(self)


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

        x = self.UTILS.getElement(DOM.Settings.call_log_number_xpath, "Call ID value")

        self.UTILS.TEST(x.text == "Hide number", "Checking Call ID valuer")


