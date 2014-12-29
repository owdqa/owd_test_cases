from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        self.test_contacts = [MockContact() for i in range(3)]
        self.test_numbers = [self.test_contacts[i]["tel"]["value"] for i in range(len(self.test_contacts))]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        # Delete all call log
        self.dialer.callLog_clearAll()

        # Call each number
        map(self._do_the_call, self.test_numbers)

        screen_1 = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries:", screen_1)

        self.dialer.callLog_clearAll()

        screen_2 = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries removed:", screen_2)


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

        #x = self.UTILS.general.get_config_variable("phone_number", "custom")
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
        keypad_options = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        keypad_options.tap()

        #Tap call button
        call_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        call_button.tap()

        #Assert that nothing is presented in the input area
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field")
        dialer_num = x.get_attribute("value")
        self.assertEqual(dialer_num, "", "Nothing in the input area")

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)

