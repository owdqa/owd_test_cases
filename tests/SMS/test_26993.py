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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        self.Dialer      = Dialer(self)

        self.num1 = '0034' + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

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
        # Create and send a new test message to this contact.
        #
        self.messages.startNewSMS()
        
        self.messages.selectAddContactButton()
        self.contacts.viewContact(self.Contact_1["familyName"], False)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.Contact_1["name"], True)

        self.messages.enterSMSMsg("Test message.")
        self.messages.sendSMS()

        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the header to call.
        #
        self.messages.header_call()
        
        #
        # Dialler is started with the number already filled in.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number")
        self.UTILS.TEST(self.num2 in x.get_attribute("value"),
                        "The phone number contains '%s' (it was '%s')." % (self.num1, x.get_attribute("value")))
