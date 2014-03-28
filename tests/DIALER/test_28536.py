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
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
       GaiaTestCase.setUp(self)
       self.UTILS = UTILS(self)

       self.dialer = Dialer(self)

       #
       # Get own number.
       #
       self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
       self.UTILS.reporting.logComment("Llamando a.." +self.target_telNum)
    
    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        # Launch dialer app.
        self.dialer.launch()

        # Do an incoming call
        self.UTILS.general.createIncomingCall(self.target_telNum)
        time.sleep(30)

        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        #Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        self.assertEqual(dialer_num, "", "Nothing in the input area")

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)