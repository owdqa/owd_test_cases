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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
        #self.telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact()
        self.telNum = self.Contact_1["tel"]["value"]
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        
        #
        # Enter country prefix 0034.
        #
        self.dialer.enterNumber("0034"+self.telNum)
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        p_num="0034"+self.telNum
        x.tap()

        #
        # The call is tested.
        #
        time.sleep(1)
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)

        time.sleep(2)

        self.dialer.hangUp()


        #
        # Enter country prefix 0039.
        #
        self.dialer.enterNumber("0039"+self.telNum)
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        p_num="0039"+self.telNum
        x.tap()
        #
        # The call is tested.
        #
        time.sleep(1)
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)

        time.sleep(2)

        self.dialer.hangUp()


        #
        # Enter country prefix +34.
        #
        self.dialer.enterNumber("+34"+self.telNum)
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call button")
        p_num="+34"+self.telNum
        x.tap()
        #
        # The call is tested.
        #
        time.sleep(1)
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)

        time.sleep(2)

        self.dialer.hangUp()