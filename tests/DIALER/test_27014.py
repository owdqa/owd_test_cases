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
        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)

        self.dialer.hangUp()

        #
        # Open the call log and select Add to Contact.
        #
        self.dialer.openCallLog()

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(self.num)),
                                   "The call log for number {}".format(self.num))
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
        x.tap()

        #
        # Switch to the Contacts frame and press the cancel button in the header.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(("xpath", "//h1[text()='Select contact']"), "'Select contact' header")
        x = self.UTILS.element.getElement(DOM.Dialer.add_to_conts_cancel_btn, "Cancel icon")
        x.tap()

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts application")

        #
        # Check we're back in the call log.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        self.UTILS.element.waitForElements(("xpath", "//h1[text()='Call log']"), "Call log header")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot and html dump:", x)
