# OWD-28539: Press call button after deleting all the calls from the call log 
# ** Procedure
#       1. Open call app
#       2. Open edit mode
#       3. Press select all button
#       4. Press delete button
#       ER1
#       5. Open dialer app
#       6. Press call button
# 
# ** Expected Results
#       ER1: All calls are deleted
#       ER2: display a message within the input area for 3 seconds.
#
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

    def _do_the_call(self, number):
        self.dialer.enterNumber(number, validate=False)
        self.dialer.call_this_number_and_hangup(5)

    def test_run(self):
        self.dialer.launch()

        # Delete all call log
        self.dialer.callLog_clearAll()

        # Call each number
        map(self._do_the_call, self.test_numbers)
        self.dialer.callLog_clearAll()

        # Go back to dialer keypad
        keypad_options = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        keypad_options.tap()

        # Tap call button
        call_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        call_button.tap()

        # Assert that nothing is presented in the input area
        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field")
        dialer_num = phone_field.get_attribute("value")
        self.assertEqual(dialer_num, "", "Nothing in the input area")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", screenshot)      
