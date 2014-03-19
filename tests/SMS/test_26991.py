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
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact
from OWDTestToolkit.apps.dialer import Dialer
#import time


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.contact = MockContact(tel = {'type': 'Mobile', 'value': self.num1})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Test message.")
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the header to call.
        #
        self.messages.header_call()

        #
        # Dialler is started with the number already filled in.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number")
        self.UTILS.test.TEST(self.num1 in x.get_attribute("value"), 
                        "The phone number contains '{}' (it was '{}').".format(self.num1, x.get_attribute("value")))

        #
        # Dial the number.
        #
        self.Dialer.callThisNumber()