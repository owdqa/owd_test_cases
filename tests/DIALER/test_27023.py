#27023: Call log entry already in contacts 
# ** Procedure
#       1. Open call log
#       2. Tap on call to number already in contacts
# ** Expected Results
#       1. An entry with call to a number already in contacts is displayed
#       2. Contact details screen is displayed with selected number highlighted
#
import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from marionette import Actions


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.test_contact)

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.dialer.open_call_log()

        self.dialer.callLog_long_tap(self.test_contact["tel"]["value"])
        call_info = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_call_info, "Call information button")
        call_info.tap()

        call_info_header = self.UTILS.element.getElement(DOM.Dialer.call_info_title, "Call info title")
        self.UTILS.test.test(call_info_header.text == self.test_contact['name'], 'Header title matches with contact')

        go_to_contact_details_button = self.UTILS.element.getElement(DOM.Dialer.call_info_contact_go_to_contact_details, "Go to contact detail")

        self.UTILS.element.waitForElements(("xpath", "//button[contains(@class,'remark') and @data-tel='{}']".\
                                            format(self.test_contact["tel"]["value"])), "Highlighted number")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot:", screenshot)
