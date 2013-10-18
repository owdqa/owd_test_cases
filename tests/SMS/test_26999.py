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
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
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
        test_str = "Nine 123456789 numbers."
        self.messages.createAndSendSMS([self.num1], test_str)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Long press the emedded number link.
        #
        y = x.find_element("tag name", "a")  
        self.actions    = Actions(self.marionette)
        self.actions.long_press(y,2).perform()
        
        #
        # Select create new contact.
        #
        x = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn, "Create new contact button")
        x.tap()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
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
