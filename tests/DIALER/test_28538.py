# 28538: Press call button while the last outgoing call is a contact number
# ** Prerrequestites
#       The last outgoing call is a contact number
# ** Procedure
#       1. Open dialer app
#       2. Press call button

# ** Expected Results
#       Tapping on the Call button retrieves the most recent outgoing number
#       from the call log and the contact name is charged
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.test_contact)

        # Generate an entry in the call log for this contact
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        kepad_option = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        kepad_option.tap()

        call_btn = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        call_btn.tap()

        # Make sure that after tapping, we get the last outgoing call in the call log
        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = phone_field.get_attribute("value")

        self.UTILS.test.test(self.test_contact["tel"]["value"] in dialer_num,
                             "After calling '{}', and tapping call button, phone number field contains '{}'.".
                             format(self.test_contact["tel"]["value"], dialer_num))

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)
