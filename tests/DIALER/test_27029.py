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

        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.dialer.callLog_createContact(self.num)

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.Contact_1["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.Contact_1["familyName"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                                format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        self.UTILS.element.waitForElements(("xpath", "//h1[text()='Call log']"), "Call log header")

        #
        # Verify that the call log now shows the contact name,
        #
        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(self.num)),
                                   "The call log for number {}".format(self.num))

        self.UTILS.test.TEST(self.Contact_1["name"] in x.text, "Call log now shows '{}'.".\
                             format(self.Contact_1["name"]))
