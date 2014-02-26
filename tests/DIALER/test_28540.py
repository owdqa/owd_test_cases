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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
 
    def setUp(self):
            
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)
        
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.Contact_2 = MockContact()
        self.Contact_3 = MockContact()
        
        #self.data_layer.insert_contact(self.cont1)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.dialer.launch()

        # Delete all call log
        self.dialer.callLog_clearAll()

        # Call 3 different numbers
        self.dialer.enterNumber(self.Contact_1["tel"]["value"])
        self.dialer.callThisNumber()
        self.dialer.hangUp()

        self.dialer.enterNumber(self.Contact_2["tel"]["value"])
        self.dialer.callThisNumber()
        self.dialer.hangUp()

        self.dialer.enterNumber(self.Contact_3["tel"]["value"])
        self.dialer.callThisNumber()
        self.dialer.hangUp()

        # Tapping call button
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        #Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        self.UTILS.TEST(str(self.Contact_3["tel"]["value"]) in dialer_num,
                        "After calling '{0:s}', and tapping call button, phone number field contains '{1:s}'.")

        y = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)