#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #Get details of our test contacts.
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num})
        self.UTILS.insertContact(self.Contact_1)

        self.contact_name = self.Contact_1["name"]
        self.contact_given_name = self.Contact_1["givenName"]
        self.contact_number = self.Contact_1["tel"]["value"]

    def tearDown(self):
        #
        # Delete the contact. (REVISAR)
        #
        #self.contacts.launch()
        #self.contacts.deleteContact(self.contact_name)

        self.UTILS.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()

        # Enter Contacts Option.
        x = self.UTILS.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        x.tap()

        # Select contact.
        print "Contact name is: " + self.contact_name
        self.contacts.viewContact(self.contact_name, p_HeaderCheck=False)

        # Call
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        #p_num = x.get_attribute("value")
        x.tap()

        #self.dialer.createMultipleCallLogEntries(x, 1)
        #self.dialer.enterNumber(self.cont2["tel"]["value"])
        #self.dialer.callThisNumber()

        time.sleep(2)
        # Hang Up
        self.dialer.hangUp()


        x = self.UTILS.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()

        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        #Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        #print "dialer_num is " + dialer_num
        #print "contact number is " + self.contact_number

        self.UTILS.TEST(self.contact_number in dialer_num, "After calling '{0:s}', and tapping call button, phone number field contains '{1:s}'.")

        y = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screen shot of the result of tapping call button", y)
