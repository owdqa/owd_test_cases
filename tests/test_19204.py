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
from tests.mock_data.contacts import MockContacts

class test_19204(GaiaTestCase):
    _Description = "[SMS] Send a new SMS by entering manually the phone number (contact number)."
    
    _TestMsg     = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        
        #
        # Prepare the contact we're going to import.
        #
        self.contact_1 = MockContacts().Contact_1

        #
        # Establish which phone number to use.
        #
        self.contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.contact_1["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
        
        
        
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
        self.messages.createAndSendSMS([self.contact_1["tel"]["value"]], self._TestMsg)
        
#         #
#         # Wait for the last message in this thread to be a 'recieved' one.
#         #
#         returnedSMS = self.messages.waitForReceivedMsgInThisThread()
#         self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)
#         
#         #
#         # TEST: The returned message is as expected (caseless in case user typed it manually).
#         #
#         sms_text = returnedSMS.text
#         self.UTILS.TEST((sms_text.lower() == self._TestMsg.lower()), 
#             "SMS text = '" + self._TestMsg + "' (it was '" + sms_text + "').")
# 
#         #
#         # Verify that the header text is now the contact name.
#         #
#         x = self.UTILS.waitForElements(("xpath","//h1[text()='" + self.contact_1["name"] + "']"), 
#                                        "Header matching contact name")
        
