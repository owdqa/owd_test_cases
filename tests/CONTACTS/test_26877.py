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
    
#     _RESTART_DEVICE = True
    
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
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = "123456789"
        self.contact_1["tel"]["value"] = self.num1
        
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
        self.contacts.launch() #(Just so we can switch to it later)
        self.messages.launch()

        
        self.messages.createAndSendSMS([self.contact_1["tel"]["value"]], "Test message")
        self.messages.waitForReceivedMsgInThisThread()
         
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
         
        self.messages.createAndSendSMS([self.num2], "Thread for a different number")

        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "=================================================================")
        self.UTILS.logResult("info", "<b>If SMS app is closed when you click 'send sms' in contacts ...</b>")
        self._doTest()
        
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "=====================================================================")
        self.UTILS.logResult("info", "<b>If SMS app is still open when you click 'send sms' in contacts ...</b>")
        self.messages.openThread(self.num2)
        self._doTest()
        

    def _doTest(self):

        #
        # Launch contacts app etc...
        #
        self.UTILS.switchToApp("Contacts")
        self.contacts.viewContact(self.contact_1['name'])
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()
        
        #
        # Switch to sms frame and complete the tests + send the message.
        #
        time.sleep(5)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.UTILS.logResult("info", "<b>NOTE: </b>expecting to be in a 'compose new sms' screen (not a thread) ...")

        
        self.UTILS.headerCheck("1 recipient")
        self.messages.enterSMSMsg("Test msg.")
        self.messages.sendSMS()

        #
        # Verify that we are now in the thread for this contact.
        #
        self.UTILS.logResult("info", 
                             "<b>NOTE: </b> expecting to be automatically taken to the thread for '%s' ..." % \
                             self.contact_1['name'])
        self.UTILS.headerCheck(self.contact_1['name'])
    
        msg_count = self.UTILS.getElements(DOM.Messages.message_list, "Thread messages", False, 5, False)
        
        if msg_count:
            self.UTILS.TEST(len(msg_count) > 1, "There are <i>some</i> messages in this thread already.")
        else:
            self.UTILS.logResult(False, "There are <i>some</i> messages in this thread already.")
        
