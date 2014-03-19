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
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num})

        self.UTILS.general.insertContact(self.Contact_1)
    
    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        self.dialer.launch()
        self.dialer.enterNumber(self.Contact_1["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.dialer.openCallLog()

        x = self.UTILS.element.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.Contact_1["tel"]["value"]),
                           "The call log for number %s" % self.Contact_1["tel"]["value"])
        x.tap()

        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)

        self.UTILS.element.waitForElements( ("xpath", "//button[contains(@class,'remark') and @data-tel='%s']" % self.Contact_1["tel"]["value"]),
                                     "Highlighted number")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot:", x)
