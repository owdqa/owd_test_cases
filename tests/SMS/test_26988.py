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
        self.contacts   = Contacts(self)

        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.cont = MockContacts().Contact_1
        self.data_layer.remove_all_contacts()
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
        # Tap the header to create a contact.
        #
        self.messages.header_addToContact()
        
        #
        # Select our contact.
        #
        self.contacts.selectContactFromAll(self.cont["familyName"])
        
        #
        # Check the phone number.
        #
        x = self.UTILS.getElement(("id", "number_1"), "2nd phone number.")
        self.UTILS.TEST(x.get_attribute("value") == self.num1,
                        "Contact now has a 2nd number which is '%s' (it was '%s')." % (self.num1, x.get_attribute("value")))
        
        #
        # Press the Done button.
        #
        x = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Update button")
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
        self.UTILS.TEST(x.text == self.cont["name"], 
                        "Message header has been changed to match the contact (it was '%s')." % x.text)
        
        #
        # Go back to the threads view and check the message name there too.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread(self.cont["name"])