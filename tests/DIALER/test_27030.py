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
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

        self.num  = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact()
        self.UTILS.general.insertContact(self.Contact_1)
    
    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.launch()

        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.dialer.callLog_addToContact(self.num, self.Contact_1["name"])

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
 
        #
        # Re-open the call log and Verify that it now shows the contact name,
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator) 
        self.UTILS.element.waitForElements( ("xpath", "//h1[text()='Call log']"), "Call log header")

        x = self.UTILS.element.getElement( ("xpath", DOM.Dialer.call_log_number_xpath.format(self.num),
                                   "The call log for number %s" % self.num)

        self.UTILS.test.TEST(self.Contact_1["name"] in x.text, "Call log now shows '%s'." % self.Contact_1["name"])