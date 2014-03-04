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
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact

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
        
        self.cont = MockContact(email = [{"type": "Personal", "value": "email1@nowhere.com"},
                               {"type": "Personal", "value": "email2@nowhere.com"},
                               {"type": "Personal", "value": "email3@nowhere.com"}])
        self.UTILS.insertContact(self.cont)

        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
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
        _link.tap()
        
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
        x = self.UTILS.getElement(DOM.Contacts.view_all_contact_HM, "Search item")
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