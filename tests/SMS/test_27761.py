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
        
        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': '', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")
        orig_iframe = self.messages.selectAddContactButton()

        #
        # Press the back button.
        #
        x = self.UTILS.getElement(DOM.Messages.cancel_add_contact, "Cancel add contact button")
        x.tap()
                
        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("src",orig_iframe)

        #
        # Check 'Send' button is not enabled.
        #
        x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button")
        self.UTILS.TEST(not x.is_enabled(), "Send button is not enabled.")