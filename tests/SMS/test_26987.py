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
        # Tap the header to create a contact.
        #
        self.messages.header_createContact()
        
        #
        # Fill in some details.
        #
        contFields = self.contacts.getContactFields()
        self.contacts.replaceStr(contFields['givenName'  ] , "Test")
        self.contacts.replaceStr(contFields['familyName' ] , "Testerton")

        #
        # Press the Done button.
        #
        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()
        
        #
        # Wait for contacts app to close and return to sms app.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src, '%s')]" % DOM.Contacts.frame_locator[1]),
                                       "Contacts iframe")
        
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Verify the header is now the name,
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Message header")
        self.UTILS.TEST(x.text == "Test Testerton", 
                        "Message header has been changed to match the contact (it was '%s')." % x.text)
        
        #
        # Go back to the threads view and check the message name there too.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread("Test Testerton")