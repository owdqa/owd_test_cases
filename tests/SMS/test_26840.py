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
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):
    
    test_msg = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        
        
        #
        # Prepare the contact we're going to import.
        #
        tlf = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': 'Mobile', 'value': tlf})

        self.UTILS.logComment("Using target telephone number " + self.contact["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, 
        # no adding a contact).
        #
        self.UTILS.insertContact(self.contact)

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
        self.messages.createAndSendSMS([self.contact["tel"]["value"]], self.test_msg)
        
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
#         self.UTILS.TEST((sms_text.lower() == self.test_msg.lower()), 
#             "SMS text = '" + self.test_msg + "' (it was '" + sms_text + "').")
# 
#         #
#         # Verify that the header text is now the contact name.
#         #
#         x = self.UTILS.waitForElements(("xpath","//h1[text()='" + self.contact_1["name"] + "']"), 
#                                        "Header matching contact name")
        
