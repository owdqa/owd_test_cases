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
        # Long press the embedded number link.
        #
        y = x.find_element("tag name", "a")  
        y.tap()
        
        #
        # Select create new contact.
        #
        x = self.UTILS.getElement(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        x.tap()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        contFields = self.contacts.getContactFields()
        
        #
        # Verify the number is in the number field.
        #
        self.UTILS.TEST("123456789" in contFields['tel'].get_attribute("value"),
                        "Our target number is in the telephone field (it was %s)." % contFields['tel'].get_attribute("value"))
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replaceStr(contFields['givenName'  ] , "Test2700")
        self.contacts.replaceStr(contFields['familyName' ] , "Testerton")
        x = self.UTILS.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()
        
        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src, '%s')]" % DOM.Contacts.frame_locator[1]),
                                       "Contacts iframe")
        
        #
        # Verify that the sms app is still running.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)