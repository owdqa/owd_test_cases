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
from OWDTestToolkit.apps import Messages
from tests._mock_data.contacts import MockContact
from OWDTestToolkit.apps.dialer import Dialer
#import time


class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.Dialer      = Dialer(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
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
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number")
        self.UTILS.TEST(self.num1 in x.get_attribute("value"), 
                        "The phone number contains '%s' (it was '%s')." % (self.num1, x.get_attribute("value")))

        #
        # Dial the number.
        #
        self.Dialer.callThisNumber()