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
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': num})

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.enterNumber(self.contact["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)

        self.dialer.hangUp()
        self.dialer.openCallLog()

        _number_el = DOM.Dialer.call_log_number_xpath.format(self.contact["tel"]["value"])
        self.UTILS.element.waitForElements(("xpath", _number_el),
                           "The number {} in the call log".format(self.contact["tel"]["value"]))
        self.UTILS.element.waitForNotElements(("xpath", "{}//*[text()='{}']".\
                                               format(_number_el, self.contact["name"])),
                                              "The name {} in the call log".format(self.contact["name"]))
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Call log <i>before</i> adding contact details for this number:", x)

        self.contacts.launch()
        self.contacts.create_contact(self.contact)

        self.dialer.launch()
        self.dialer.openCallLog()

        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.call_log_name_xpath.format(self.contact["name"])),
                           "The name {} in the call log".format(self.contact["name"]))
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Call log <i>after</i> adding contact details for this number:", x)
