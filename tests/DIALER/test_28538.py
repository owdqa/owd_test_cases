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

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.

        # self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': "665666666"})
        self.UTILS.general.insertContact(self.contact)

        self.contact_name = self.contact["name"]
        self.contact_given_name = self.contact["givenName"]
        self.contact_number = self.contact["tel"]["value"]

    def tearDown(self):
        #
        # Delete the contact. (REVISAR)
        #
        # self.contacts.launch()
        # self.contacts.delete_contact(self.contact_name)

        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()

        # Enter Contacts Option.
        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        x.tap()

        # Select contact.
        self.contacts.view_contact(self.contact_name, header_check=False)

        # Call
        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()

        time.sleep(2)
        # Hang Up
        self.dialer.hangUp()

        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        # Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        self.UTILS.test.TEST(self.contact_number in dialer_num,
                             "After calling '{}', and tapping call button, phone number field contains '{}'.".\
                             format(self.contact_number, dialer_num))

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)
