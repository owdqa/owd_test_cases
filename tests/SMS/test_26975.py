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
        self.browser    = Browser(self)
        self.actions    = Actions(self.marionette)

        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_email = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        
        self.msg = "Testing email link with " + self.target_email
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.UTILS.getNetworkConnection()
                
        #
        # Launch messages app.
        #
        self.messages.launch()
          
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self.msg)
          
        #
        # Wait for the last message in this thread to be a 'recieved' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        #
        # Long-press the link.
        #
        email_link = x.find_element("tag name", "a")
        self.actions.press(email_link).wait(2).release().perform()

        x = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn, "'Add to an existing contact' button")
        x.tap()
                
        #
        # Check for warning message.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator_dfo)
        
        self.UTILS.waitForElements( ("xpath", "//p[contains(text(),'contact list is empty')]"), "Warning message")
        

