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
from OWDTestToolkit.apps.browser import Browser
from marionette import Actions

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)
        self.actions = Actions(self.marionette)

        
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
        email_link.tap()

        x = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn,
                                    "'Add to an existing contact' button")
        x.tap()
                
        #
        # Check for warning message.
        #
        self.UTILS.switchToFrame("src", "contacts")
        
        self.UTILS.waitForElements(("xpath", 
                "//p[contains(text(),'contact list is empty')]"), "Warning message")
        
        fnam = self.UTILS.screenShot("26975")
        self.UTILS.logResult("info", "Screenshot of final position", fnam)
