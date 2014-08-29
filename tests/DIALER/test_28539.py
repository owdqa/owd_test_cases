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
        self.Contact_1 = MockContact()
        self.Contact_2 = MockContact()
        self.Contact_3 = MockContact()
        self.Contact_4 = MockContact()


        #self.data_layer.insert_contact(self.cont1)
        #self.data_layer.insert_contact(self.cont2)
        #self.data_layer.insert_contact(self.cont3)

        self.contact_number_1 = self.Contact_1["tel"]["value"]
        self.contact_number_2 = self.Contact_2["tel"]["value"]
        #self.contact_number_3 = self.cont3["tel"]["value"]
        self.contact_number_twilio = self.Contact_4["tel"]["value"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        #x = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        # create logs entries from contacts
        self.dialer.createMultipleCallLogEntries(self.contact_number_1, 3)
        self.dialer.createMultipleCallLogEntries(self.contact_number_2, 2)
        #self.dialer.createMultipleCallLogEntries(self.contact_number_3, 2)
        self.dialer.createMultipleCallLogEntries(self.contact_number_twilio, 4)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries:", x)

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

