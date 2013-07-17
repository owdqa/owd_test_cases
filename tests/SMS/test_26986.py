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
        self.contacts   = Contacts(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = "621234567"
        
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
        self.messages.createAndSendSMS([self.num1], "Test %s number." % self.num2)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the header to create a contact.
        #
        self.messages.header_createContact()
        
        #
        # Cancel the action.
        #
        x = self.UTILS.getElement(DOM.Contacts.edit_cancel_button, "Cancel button")
        x.tap()
        
        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src, '%s')]" % DOM.Contacts.frame_locator[1]),
                                       "Contacts iframe")
        
        #
        # Kill the SMS app (and all others).
        #
        self.apps.kill_all()
        
        #
        # Open the contacts app.
        #
        self.contacts.launch()
        
        #
        # Verify that there are no contacts.
        #
        self.UTILS.waitForElements( ("xpath", "//p[contains(text(), 'No contacts')]"),
                                    "No contacts message")
        
        
        