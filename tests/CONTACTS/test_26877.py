#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

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
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)
        

        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Contact_1

        #
        # Establish which phone number to use.
        #
        self.contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
            
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a thread for this contact.
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.contact_1["tel"]["value"]], "Test message")
        self.messages.waitForReceivedMsgInThisThread()
        self.apps.kill_all()

        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.contact_1['name'])
        
        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Verify that we are now in the thread for this contact.
        #
        self.UTILS.logResult("info", "<b>NOTE: </b> expecting to be autimatically taken to the thread for this contact ...")
        self.UTILS.headerCheck(self.contact_1['name'])
    
        msg_count = self.UTILS.getElement(DOM.Messages.message_list, "Thread messages", True, 5, False)
        self.UTILS.TEST(msg_count > 1, "There are <i>some</i> messages in this thread already.")
        
        #
        # Create SMS.
        #
        self.messages.enterSMSMsg("Test msg.")
        
        #
        # Click send.
        #
        self.messages.sendSMS()
