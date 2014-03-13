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
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.num1 = "+34" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

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
        self.messages.createAndSendSMS([self.num1], "Test message")
        x = self.messages.waitForReceivedMsgInThisThread()
        
        # 
        # Tap the header.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        #
        # Verify that each expected item is present.
        #
        self.UTILS.waitForElements(DOM.Messages.header_call_btn,
                                    "Call button")
        self.UTILS.waitForElements(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        self.UTILS.waitForElements(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        self.UTILS.waitForElements(DOM.Messages.header_cancel_btn_no_send,
                                    "Cancel button")

