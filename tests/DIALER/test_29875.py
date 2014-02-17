
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

    SERVICE_ENABLED = "Service has been disabled"
    EXPECTED_RESULT_1 = "Show number" #Change to Show number
    _RESTART_DEVICE = True

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)
        self.settings   = Settings(self)


    def tearDown(self):

        self.UTILS.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()
        self.dialer.enterNumber("#31#")

        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(2)

        x = self.UTILS.getElement(('id', 'message'), "Getting confirmation of service disabled")
        self.UTILS.logComment("Message content: " + x.text)
        self.UTILS.TEST(x.text == self.SERVICE_ENABLED, "Asserting service disabled")

        self.UTILS.goHome()
        self.UTILS.logResult("info", "Home screen")

        #Tap settings
        self.settings.launch()
        self.UTILS.logResult("info", "Settings screen")

        x = self.UTILS.getElement(DOM.Settings.call_settings, "Call number button")
        x.tap()
        self.UTILS.logResult("info", "Call number presses")

        time.sleep(2)

        x = self.UTILS.getElement(('css selector', '.fake-select button.icon.icon-dialog'), "Getting default option")
        self.UTILS.logComment("Button content: " + x.text)
        self.UTILS.TEST(x.text == self.EXPECTED_RESULT_1, "Checking Call Line Identification Restriction is configured as Show number")


        self.UTILS.goHome()
        self.UTILS.logResult("info", "Home screen")

        self.dialer.launch()
        self.dialer.enterNumber("*#31#")


        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(2)

        #Tap settings
        self.settings.launch()
        self.UTILS.logResult("info", "Settings screen")

        x = self.UTILS.getElement(DOM.Settings.call_settings, "Call number button")
        x.tap()
        self.UTILS.logResult("info", "Call number presses")

        time.sleep(2)

        x = self.UTILS.getElement(('css selector', '.fake-select button.icon.icon-dialog'), "Getting default option")
        self.UTILS.logComment("Button content: " + x.text)
        self.UTILS.TEST(x.text == self.EXPECTED_RESULT_1, "Checking Call Line Identification Restriction is configured as Show number")
