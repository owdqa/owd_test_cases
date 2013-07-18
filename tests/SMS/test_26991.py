#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.phone      = Phone(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.cont = MockContacts().Contact_1
        self.cont["tel"]["value"] = self.num1
        self.data_layer.insert_contact(self.cont)        
        
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
        x = self.UTILS.getElement(DOM.Phone.phone_number, "Phone number")
        self.UTILS.TEST(self.num1 in x.get_attribute("value"), 
                        "The phone number contains '%s' (it was '%s')." % (self.num1, x.get_attribute("value")))

        #
        # Dial the number.
        #
        self.phone.callThisNumber()

        #
        # Wait 2 seconds, then hangup.
        #
        time.sleep(2)
        self.data_layer.kill_active_call()