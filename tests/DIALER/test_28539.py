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
import time

class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #Get details of our test contacts.
        #self.cont1 = MockContacts().Contact_1
        self.cont2 = MockContacts().Contact_2
        self.cont3 = MockContacts().Contact_3


        #self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        self.data_layer.insert_contact(self.cont3)

        #self.contact_number_1 = self.cont1["tel"]["value"]
        self.contact_number_2 = self.cont2["tel"]["value"]
        self.contact_number_3 = self.cont3["tel"]["value"]

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.dialer.launch()

        #x = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        # create logs entries from contacts
        #self.dialer.createMultipleCallLogEntries(self.contact_number_1, 2)
        self.dialer.createMultipleCallLogEntries(self.contact_number_2, 1)
        self.dialer.createMultipleCallLogEntries(self.contact_number_3, 2)

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of multiple entries:", x)

        ##self.dialer.callLog_clearAll2()

        ##x = self.UTILS.screenShotOnErr()
        ##self.UTILS.logResult("info", "Screenshot of multiple entries removed:", x)

        #Go back to dialer keypad
        ##x = self.UTILS.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        ##x.tap()

        #Tap call button
        ##x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        ##x.tap()

        #Assert that nothing is presented in the input area
        #x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field")
        #dialer_num = x.get_attribute("value")
        #self.UTILS.assertEqual(dialer_num, "", "Nothing in the input area")

        #y = self.UTILS.screenShotOnErr()
        #self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)

