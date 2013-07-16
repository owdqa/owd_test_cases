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
        self.emailAddy = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
        self.cont = MockContacts().Contact_multipleEmails
        self.data_layer.insert_contact(self.cont)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
#         self.messages.deleteAllThreads()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Hello " + self.emailAddy + " old bean.")
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Long press the email link.
        #
        _link = x.find_element("tag name", "a")
        self.actions    = Actions(self.marionette)
        self.actions.long_press(_link,2).perform()
        
        #
        # Click 'Add to an existing contact'.
        #
        x = self.UTILS.getElement( ("xpath", "//button[text()='Add to an existing contact']"),
                                   "Create new contact button")
        x.tap()
        
        #
        # Verify that the email is in the email field.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.getElement( ("xpath", "//p[@data-order='%s']" % self.cont["name"].replace(" ", "")),
                                   "Search item")
        x.tap()
        
        self.UTILS.waitForElements(("xpath","//input[@type='email' and @value='%s']" % self.emailAddy), "New email address")
        
        #
        # Add gallery image.
        #
        self.contacts.addGalleryImageToContact(0)

        
        #
        # Press the Update button.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()

        #
        # Check that the contacts iframe is now gone.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'contacts')]"),
                                       "Contact app iframe")
        
        #
        # Now return to the SMS app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)