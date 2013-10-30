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
from tests._mock_data.contacts import MockContacts


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #Get details of our test contacts.
        self.cont1 = MockContacts().Contact_1

        self.data_layer.insert_contact(self.cont1)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.dialer.launch()

        #self.dialer.createMultipleCallLogEntries(x, 1)
        self.dialer.enterNumber(self.cont1["tel"]["value"])
        self.dialer.callThisNumber()
        #time.wait(2)
        self.dialer.hangUp()

        x = self.UTILS.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()
        #time.wait(1)

        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        #Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.TEST(str(self.cont1["tel"]["value"]) in dialer_num,
                        "After calling '%s', and tapping call button, phone number field contains '%s'." %
                        (dialer_num, str(self.cont1["tel"]["value"])))

        y = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)