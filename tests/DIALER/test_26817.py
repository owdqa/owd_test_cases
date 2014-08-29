# 26817: Create a contact with a number that is in the call log and is not linked to any contact before
# ** Procedure
#       1-Open the call log and select a phone that is not in the address book
#       2-Close the call log
#       3-Open address book
#       4-Create a new contact without photo with the phone selected in the first step
#       5-Open the call log again to verify if the former register is updated with the new information
# ** Expected Results
#       When accessing call log after contact creation, new information is updated in the register in the call log.
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': num})

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.createMultipleCallLogEntries(self.test_contact["tel"]["value"], 1)
        self.dialer.openCallLog()

        _number_el = DOM.Dialer.call_log_number_xpath.format(self.test_contact["tel"]["value"])
        elem = ('xpath', _number_el)
        self.UTILS.element.waitForElements(elem,
                                           "The number {} in the call log".format(self.test_contact["tel"]["value"]))
        self.UTILS.element.waitForNotElements(("xpath", "{}//*[text()='{}']".
                                               format(_number_el, self.test_contact["name"])),
                                              "The name {} in the call log".format(self.test_contact["name"]))

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult(
            "info", "Call log <i>before</i> adding contact details for this number:", screenshot)

        self.contacts.launch()
        self.contacts.create_contact(self.test_contact)

        self.dialer.launch()
        self.dialer.openCallLog()

        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.call_log_name_xpath.format(self.test_contact["name"])),
                                           "The name {} in the call log".format(self.test_contact["name"]))
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Call log <i>after</i> adding contact details for this number:", x)
