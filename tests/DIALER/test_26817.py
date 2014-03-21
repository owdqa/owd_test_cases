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

    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.enterNumber(self.contact["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)

        self.UTILS.test.TEST(True, "Looking for Element OK Button")
        ok_btn = self.UTILS.element.getElement(DOM.Dialer.call_busy_button_ok, "Ok Button")

        # Since the call destination is the same as the origin, it's very likely to get an error
        # message. If this is the case, tap the OK button. Otherwise (i.e. using twilio), hang up the call
        if ok_btn:
            self.UTILS.test.TEST(True, "Button text: {}".format(ok_btn.text))
            ok_btn.tap()
        else:
            self.dialer.hangUp()

        self.dialer.openCallLog()

        self.UTILS.TEST(True, "Looking for {} in DOM Element: {}".format(self.contact["tel"]["value"],
                                                                         DOM.Dialer.call_log_number_xpath))
        _number_el = DOM.Dialer.call_log_number_xpath.format(self.contact["tel"]["value"])
        self.UTILS.TEST(True, "Waiting for elements _number_el: {}".format(_number_el))
        self.UTILS.element.waitForElements(("xpath", _number_el),
                           "The number {} in the call log".format(self.contact["tel"]["value"]))
        self.UTILS.TEST(True, "Waiting for NOT elements: {}".format("{}//*[text()='{}']".\
                                                                    format(_number_el, self.contact["name"])))
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
