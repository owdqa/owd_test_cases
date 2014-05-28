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


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #Get details of our test contacts.
        self.test_contacts = [MockContact() for i in range(4)]

        self.dialer.launch()
        map(self.dialer.createMultipleCallLogEntries, 
            [c["tel"]["value"] for c in self.test_contacts], [2 for c in self.test_contacts])

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries:", x)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.callLog_clearAll()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries removed:", x)

        #Go back to dialer keypad
        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()

        #Tap call button
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        #Assert that nothing is presented in the input area
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field")
        dialer_num = x.get_attribute("value")
        self.assertEqual(dialer_num, "", "Nothing in the input area")

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)

