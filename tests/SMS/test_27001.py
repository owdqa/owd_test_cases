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
        test_str = "Nine 111111111 numbers."
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
        x = self.UTILS.getElement(DOM.Messages.header_cancel_btn_no_send, "Add to existing contact button")
        x.tap()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Select our contact.
        #
        self.contacts.viewContact(self.cont["familyName"], False)
        
        #
        # Check the phone number.
        #
        x = self.UTILS.getElement(("id", "number_1"), "2nd phone number.")
        self.UTILS.TEST(x.get_attribute("value") == "111111111",
                        "Contact now has a 2nd number which is '111111111' (it was '%s')." % x.get_attribute("value"))
        
        
        #
        # Press the update button.
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
