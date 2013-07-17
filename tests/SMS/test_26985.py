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

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = "621234567"
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure we have no contacts.
        #
        self.data_layer.remove_all_contacts()
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Test %s number." % self.num2)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Enter edit mode.
        #
        x = self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()
        
        #
        # Tap the edit header.
        #
        self.UTILS.logResult("info", "<b>NOTE:</b> This is the original number header, but really should be threads-edit-mode (marionette might be corrected for this, so switch the code to that if it starts failing)")
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header (edit header)")
        x.tap()

        #
        # Verify that nothing happened.
        #
        self.UTILS.waitForNotElements(DOM.Messages.header_call_btn, "Call button")
        self.UTILS.waitForNotElements(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        self.UTILS.waitForNotElements(DOM.Messages.header_add_to_contact_btn, "Add to existing contact button")
        self.UTILS.waitForNotElements(DOM.Messages.header_cancel_btn, "Cancel button")
        
        
        
        
        
        